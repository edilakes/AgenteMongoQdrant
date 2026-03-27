import os
import httpx
from qdrant_client import QdrantClient
from fastembed import TextEmbedding
from pymongo import MongoClient
from bson import ObjectId

class MetaRouter:
    """
    Orquestador que utiliza Qdrant para determinar qué herramientas 
    y qué fuentes de datos son necesarias para responder una consulta.
    Usa un Adaptador Nativo para MongoDB para mayor estabilidad.
    """
    
    def __init__(self, mcp_manager=None):
        self.qdrant_url = os.getenv("QDRANT_URL")
        self.qdrant_api_key = os.getenv("QDRANT_API_KEY")
        self.client = QdrantClient(url=self.qdrant_url, api_key=self.qdrant_api_key)
        self.context_map_collection = "context_map"
        
        # Conexión nativa a MongoDB (Fallback estable)
        self.mongo_client = MongoClient(os.getenv("MONGO_URL"))

        try:
            self.encoder = TextEmbedding(model_name="intfloat/multilingual-e5-large")
        except Exception as e:
            print(f"Error cargando modelo de embeddings: {e}")
            self.encoder = None

    def _get_vector(self, text: str):
        if not self.encoder:
            return None
        return list(self.encoder.embed([text]))[0].tolist()

    async def route_query(self, query: str):
        """Analiza la query buscando en el 'context_map'."""
        print(f"Buscando contexto semántico para: {query}")
        vector = self._get_vector(query)
        if not vector:
            return None

        url = f"{self.qdrant_url}/collections/{self.context_map_collection}/points/search"
        headers = {"Content-Type": "application/json"}
        if self.qdrant_api_key:
            headers["api-key"] = self.qdrant_api_key
        
        payload = {"vector": vector, "limit": 2, "with_payload": True}
        
        try:
            async with httpx.AsyncClient() as client:
                res = await client.post(url, json=payload, headers=headers)
                if res.status_code == 200:
                    results = res.json().get("result", [])
                    if results and results[0]["score"] > 0.7:
                        hit = results[0]
                        payload = hit["payload"]
                        print(f"✅ Ruta encontrada: {payload.get('text')}")
                        
                        plan = {
                            "action": "native_mongodb",
                            "access_path": payload["access_path"],
                            "semantic_summary": payload.get("text")
                        }
                        return self._clean_doc(plan)
        except Exception as e:
            print(f"Error en ruta semántica: {e}")

        # 2. Fallback: Búsqueda general en la biblioteca si no hay puntero específico
        plan = {
            "action": "qdrant_search",
            "collection": "doctrina_itheca",
            "query": query
        }
        return self._clean_doc(plan)

    def _clean_doc(self, doc):
        """Limpia recursivamente cualquier objeto para asegurar compatibilidad JSON."""
        if isinstance(doc, dict):
            return {str(k): self._clean_doc(v) for k, v in doc.items()}
        elif isinstance(doc, list):
            return [self._clean_doc(v) for v in doc]
        elif isinstance(doc, (str, int, float, bool)) or doc is None:
            return doc
        return str(doc) # Cualquier otra cosa (ObjectId, datetime, etc) -> string

    async def execute_plan(self, plan: dict):
        """Ejecuta la acción decidida por el router."""
        if plan["action"] == "native_mongodb":
            path = plan["access_path"]
            params = path["params"]
            db_name = params.get("db", "OposicionesDB")
            if "Biblia" in params.get("collection", ""):
                 db_name = "Pioteca"
            
            db = self.mongo_client[db_name]
            coll = db[params["collection"]]
            
            query_filter = params.get("filter", {})
            if "_id" in query_filter and isinstance(query_filter["_id"], str):
                try: query_filter["_id"] = ObjectId(query_filter["_id"])
                except: pass
            
            doc = coll.find_one(query_filter)
            return [self._clean_doc(doc)] if doc else []
            
        elif plan["action"] == "qdrant_search":
            vector = self._get_vector(plan["query"])
            url = f"{self.qdrant_url}/collections/{plan['collection']}/points/search"
            headers = {"Content-Type": "application/json"}
            if self.qdrant_api_key:
                headers["api-key"] = self.qdrant_api_key
            
            payload = {"vector": vector, "limit": 3, "with_payload": True}
            
            async with httpx.AsyncClient() as client:
                res = await client.post(url, json=payload, headers=headers)
                return res.json().get("result", [])
        return None
