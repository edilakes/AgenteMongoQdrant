import os
from qdrant_client import QdrantClient
from qdrant_client.models import PointStruct
from dotenv import load_dotenv
import uuid

def test_upsert():
    load_dotenv()
    client = QdrantClient(url=os.getenv("QDRANT_URL"), api_key=os.getenv("QDRANT_API_KEY"))
    
    collection = "context_map"
    print(f"Testing upsert to {collection}...")
    
    # Create a dummy vector (768 zeros)
    vector = [0.1] * 768
    point_id = str(uuid.uuid4())
    
    client.upsert(
        collection_name=collection,
        points=[
            PointStruct(
                id=point_id,
                vector=vector,
                payload={"test": "ok"}
            )
        ]
    )
    print("Upsert successful.")
    
    info = client.get_collection(collection_name=collection)
    print(f"Points count after test: {info.points_count}")

if __name__ == "__main__":
    test_upsert()
