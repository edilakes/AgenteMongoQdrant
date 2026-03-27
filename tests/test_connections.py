import os
import sys
from pymongo import MongoClient
from qdrant_client import QdrantClient
from dotenv import load_dotenv

# Añadir src al path para importar módulos si fuera necesario
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

load_dotenv()

def test_mongodb():
    print("--- Probando MongoDB ---")
    url = os.getenv("MONGO_URL")
    try:
        client = MongoClient(url, serverSelectionTimeoutMS=5000)
        # Intentar listar las bases de datos para confirmar conexión
        databases = client.list_database_names()
        print(f"Éxito: Conectado a MongoDB. Bases de datos: {databases}")
        return True
    except Exception as e:
        print(f"Error en MongoDB: {e}")
        return False

def test_qdrant():
    print("\n--- Probando Qdrant ---")
    url = os.getenv("QDRANT_URL")
    api_key = os.getenv("QDRANT_API_KEY")
    try:
        client = QdrantClient(url=url, api_key=api_key)
        collections = client.get_collections()
        print(f"Éxito: Conectado a Qdrant. Colecciones: {collections}")
        return True
    except Exception as e:
        print(f"Error en Qdrant: {e}")
        return False

if __name__ == "__main__":
    mongo_ok = test_mongodb()
    qdrant_ok = test_qdrant()
    
    if mongo_ok and qdrant_ok:
        print("\n¡Todas las conexiones críticas funcionan!")
        sys.exit(0)
    else:
        print("\nAlgunas conexiones fallaron. Revisa la configuración.")
        sys.exit(1)
