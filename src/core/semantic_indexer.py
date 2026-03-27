import os
import httpx
from typing import List, Dict, Any
from qdrant_client import QdrantClient
from fastembed import TextEmbedding
import google.generativeai as genai
from src.core.mcp_client import MCPClientManager

class SemanticIndexer:
    """
    Motor que recorre las fuentes (MongoDB, SQL, etc.), genera resúmenes
    semánticos con LLM y los indexa en Qdrant para enrutamiento.
    """
    def __init__(self):
        self.qdrant_url = os.getenv("QDRANT_URL")
        self.qdrant_api_key = os.getenv("QDRANT_API_KEY")
        self.client = QdrantClient(url=self.qdrant_url, api_key=self.qdrant_api_key)
        self.collection_name = "context_map" # Nueva colección para el Mapa del Conocimiento
        self.encoder = TextEmbedding(model_name="intfloat/multilingual-e5-large")
        
        # Configuración LLM para resúmenes
        genai.configure(api_key=os.getenv("GEMINI_API_KEY"))
        self.model = genai.GenerativeModel('gemini-2.0-flash')

        # Asegurar que la colección existe
        self._ensure_collection()

    def _ensure_collection(self):
        """Crea la colección si no existe."""
        # Nota: Usamos la API REST para ser consistentes con MetaRouter
        url = f"{self.qdrant_url}/collections/{self.collection_name}"
        headers = {"api-key": self.qdrant_api_key} if self.qdrant_api_key else {}
        
        with httpx.Client() as client:
            res = client.get(url, headers=headers)
            if res.status_code == 404:
                print(f"Creando colección {self.collection_name}...")
                create_payload = {
                    "vectors": {"size": 1024, "distance": "Cosine"}
                }
                client.put(url, json=create_payload, headers=headers)

    def _get_vector(self, text: str):
        return list(self.encoder.embed([text]))[0].tolist()

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
        except Exception:
            return content_chunk[:100]

    async def index_mongodb_collection(self, db_name: str, collection_name: str):
        """Indexa una colección entera de MongoDB directamente usando pymongo."""
        from pymongo import MongoClient
        print(f"Iniciando indexación directa de {db_name}.{collection_name}...")
        
        mongo_url = os.getenv("MONGO_URL")
        client = MongoClient(mongo_url)
        db = client[db_name]
        collection = db[collection_name]
        
        # Recuperamos documentos (limitado para el piloto)
        cursor = collection.find({}).limit(100)
        
        points = []
        for i, doc in enumerate(cursor):
            # 1. Extraer texto relevante
            # Buscamos campos comunes de texto o serializamos lo más importante
            content = doc.get("text", doc.get("texto", str(doc)))
            if isinstance(content, list):
                content = " ".join([str(p) for p in content])
            
            # 2. Generar resumen semántico
            summary = await self.generate_summary(str(content))
            vector = self._get_vector(summary)
            
            # 3. Crear punto con metadatos de acceso
            point_id = f"{collection_name}_{i}"
            payload = {
                "text": summary,
                "source_type": "mongodb",
                "access_path": {
                    "server": "mongodb",
                    "tool": "find",
                    "params": {
                        "collection": collection_name,
                        "filter": {"_id": str(doc["_id"])} if "_id" in doc else doc
                    }
                },
                "metadata": {
                    "original_collection": collection_name,
                    "database": db_name,
                    "title": doc.get("titulo", doc.get("name", "Documento sin título"))
                }
            }
            
            points.append({
                "id": i,
                "vector": vector,
                "payload": payload
            })

        # Subida masiva via HTTP
        upload_url = f"{self.qdrant_url}/collections/{self.collection_name}/points"
        headers = {"api-key": self.qdrant_api_key, "Content-Type": "application/json"} if self.qdrant_api_key else {}
        
        with httpx.Client() as client:
            res = client.put(upload_url, json={"points": points}, headers=headers)
            print(f"Indexación completada: {res.status_code} - {res.text}")
