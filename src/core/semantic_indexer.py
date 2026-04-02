import os
import httpx
from typing import List, Dict, Any
from qdrant_client import QdrantClient
import google.generativeai as genai
from src.core.mcp_client import MCPClientManager

class SemanticIndexer:
    """
    Motor que recorre las fuentes (MongoDB, SQL, etc.), genera resúmenes
    semánticos con LLM y los indexa en Qdrant para enrutamiento.
    Utiliza Gemini para Embeddings para paridad con n8n.
    """
    def __init__(self):
        self.qdrant_url = os.getenv("QDRANT_URL")
        self.qdrant_api_key = os.getenv("QDRANT_API_KEY")
        self.client = QdrantClient(url=self.qdrant_url, api_key=self.qdrant_api_key)
        self.collection_name = "context_map"
        
        # Configuración Google Gemini
        api_key = os.getenv("GEMINI_API_KEY")
        genai.configure(api_key=api_key)
        self.model = genai.GenerativeModel('gemini-2.0-flash')
        self.embedding_model = "models/gemini-embedding-001" # Paridad con n8n

        # Asegurar que la colección existe
        self._ensure_collection()

    def recreate_collection(self, collection_name: str, size: int = 3072):
        """Elimina y recrea una colección en Qdrant."""
        url = f"{self.qdrant_url}/collections/{collection_name}"
        headers = {"api-key": self.qdrant_api_key} if self.qdrant_api_key else {}
        
        with httpx.Client() as client:
            # Eliminar si existe
            client.delete(url, headers=headers)
            print(f"Recreando colección {collection_name} con tamaño {size}...")
            create_payload = {
                "vectors": {"size": size, "distance": "Cosine"}
            }
            res = client.put(url, json=create_payload, headers=headers)
            if res.status_code != 200:
                print(f"Error recreando colección: {res.text}")

    def _ensure_collection(self):
        """Asegura que la colección por defecto existe."""
        url = f"{self.qdrant_url}/collections/{self.collection_name}"
        headers = {"api-key": self.qdrant_api_key} if self.qdrant_api_key else {}
        
        with httpx.Client() as client:
            res = client.get(url, headers=headers)
            if res.status_code == 404:
                self.recreate_collection(self.collection_name, 3072)

    def _get_vector(self, text: str):
        """Genera embedding usando la API de Gemini."""
        try:
            result = genai.embed_content(
                model=self.embedding_model,
                content=text,
                task_type="retrieval_document"
            )
            return result['embedding']
        except Exception as e:
            print(f"Error generando embedding: {e}")
            return None

    def _extract_text(self, doc: Any, collection_name: str) -> str:
        """Extrae el texto relevante según la colección."""
        if collection_name == "normas":
            # Caso específico para normas: unir texto.p
            texto_obj = doc.get("texto", {})
            if isinstance(texto_obj, dict) and "p" in texto_obj:
                paragraphs = texto_obj["p"]
                if isinstance(paragraphs, list):
                    return " ".join([str(p) for p in paragraphs])
            return str(doc.get("texto", doc.get("text", str(doc))))
        
        # Caso general
        content = doc.get("content", doc.get("text", doc.get("texto", doc.get("pregunta", str(doc)))))
        if isinstance(content, list):
            content = " ".join([str(p) for p in content])
        return str(content)

    async def generate_summary(self, content_chunk: str) -> str:
        """Usa Gemini para crear un resumen semántico denso orientado a búsqueda."""
        prompt = f"""
        Analiza el siguiente fragmento de contenido y genera un RESUMEN SEMÁNTICO MUY BREVE (máximo 20 palabras) 
        que describa perfectamente qué tipo de información contiene. 
        Este resumen se usará para búsqueda vectorial.
        
        CONTENIDO:
        {content_chunk[:2000]}
        
        RESUMEN:"""
        try:
            response = self.model.generate_content(prompt)
            return response.text.strip()
        except Exception as e:
            print(f"Error generando resumen: {e}")
            return content_chunk[:150]

    async def index_mongodb_collection(self, db_name: str, collection_name: str, qdrant_collection: str = None, limit: int = None):
        """Indexa una colección entera de MongoDB directamente usando pymongo."""
        from pymongo import MongoClient
        target_qdrant = qdrant_collection or self.collection_name
        print(f"Iniciando indexación de {db_name}.{collection_name} -> Qdrant.{target_qdrant}...")
        
        mongo_url = os.getenv("MONGO_URL")
        client = MongoClient(mongo_url)
        db = client[db_name]
        collection = db[collection_name]
        
        query = collection.find({})
        if limit:
            query = query.limit(limit)
        
        points = []
        batch_size = 50
        
        for i, doc in enumerate(query):
            # 1. Extraer texto relevante
            content = self._extract_text(doc, collection_name)
            
            # 2. Generar resumen semántico y embedding
            # Si es muy corto, no generamos resumen, usamos el texto directo
            if len(content) < 100:
                summary = content
            else:
                summary = await self.generate_summary(content)
            
            vector = self._get_vector(summary)
            if not vector:
                continue
            
            # 3. Crear punto con metadatos de acceso
            import uuid
            point_id = str(uuid.uuid5(uuid.NAMESPACE_DNS, str(doc["_id"]))) if "_id" in doc else str(uuid.uuid4())
            
            payload = {
                "text": summary,
                "content": content[:1500],
                "source_type": "mongodb",
                "access_path": {
                    "server": "mongodb",
                    "params": {
                        "db": db_name,
                        "collection": collection_name,
                        "filter": {"_id": str(doc["_id"])} if "_id" in doc else doc
                    }
                },
                "metadata": {
                    "original_collection": collection_name,
                    "database": db_name,
                    "title": doc.get("titulo", doc.get("name", doc.get("pregunta", "Documento sin título")))
                }
            }
            
            points.append({
                "id": point_id,
                "vector": vector,
                "payload": payload
            })
            
            # Subida por lotes
            if len(points) >= batch_size:
                await self._upload_points(target_qdrant, points)
                points = []
                print(f"Procesados {i+1} documentos...")

        if points:
            await self._upload_points(target_qdrant, points)
            
        print(f"Indexación completada para {collection_name}.")

    async def _upload_points(self, collection_name: str, points: List[Dict]):
        """Sube puntos a Qdrant usando el cliente oficial."""
        from qdrant_client.models import PointStruct
        
        qdrant_points = []
        for p in points:
            qdrant_points.append(PointStruct(
                id=p["id"],
                vector=p["vector"],
                payload=p["payload"]
            ))
            
        try:
            # Upsert es síncrono en el cliente básico, pero funciona bien en bucles async
            self.client.upsert(
                collection_name=collection_name,
                points=qdrant_points,
                wait=True
            )
        except Exception as e:
            print(f"Error subiendo puntos a Qdrant: {e}")
