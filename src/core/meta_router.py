import os
import httpx
from qdrant_client import QdrantClient
import google.generativeai as genai
from pymongo import MongoClient
from bson import ObjectId

class MetaRouter:
    """
    Orquestador que utiliza Qdrant para determinar qué herramientas 
    y qué fuentes de datos son necesarias para responder una consulta.
    Sincronizado con Gemini Embeddings para paridad con n8n.
    """
    
    def __init__(self, mcp_manager=None):
        self.qdrant_url = os.getenv("QDRANT_URL")
        self.qdrant_api_key = os.getenv("QDRANT_API_KEY")
        self.client = QdrantClient(url=self.qdrant_url, api_key=self.qdrant_api_key)
        self.context_map_collection = "context_map"
        
        # Conexión nativa a MongoDB (Fallback estable)
        self.mongo_client = MongoClient(os.getenv("MONGO_URL"))

        # Configuración Google Gemini
        api_key = os.getenv("GEMINI_API_KEY")
        genai.configure(api_key=api_key)
        self.embedding_model = "models/gemini-embedding-001"

    def _get_vector(self, text: str):
        """Genera embedding usando la API de Gemini."""
        try:
            result = genai.embed_content(
                model=self.embedding_model,
                content=text,
                task_type="retrieval_query" # Cambio a 'query' para el router
            )
            return result['embedding']
        except Exception as e:
            print(f"Error generando embedding en router: {e}")
            return None

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
        
        # Sincronizado con el nuevo espacio vectorial de Gemini
        payload = {"vector": vector, "limit": 2, "with_payload": True}
        
        try:
            async with httpx.AsyncClient() as client:
                res = await client.post(url, json=payload, headers=headers)
                if res.status_code == 200:
                    results = res.json().get("result", [])
                    # Umbral de confianza ajustado para Gemini Embeddings
                    if results and results[0]["score"] > 0.65: 
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
            "collection": "doctrina_itheca", # Colección general
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
        return str(doc)

    async def execute_plan(self, plan: dict):
        """Ejecuta la acción decidida por el router."""
        if plan["action"] == "native_mongodb":
            path = plan["access_path"]
            params = path["params"]
            db_name = params.get("db", "OposicionesDB")
            
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
