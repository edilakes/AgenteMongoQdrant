import os
from qdrant_client import QdrantClient
from dotenv import load_dotenv
import json

def inspect_qdrant():
    load_dotenv()
    qdrant_url = os.getenv("QDRANT_URL")
    qdrant_api_key = os.getenv("QDRANT_API_KEY")
    
    print(f"Connecting to Qdrant at {qdrant_url}...")
    client = QdrantClient(url=qdrant_url, api_key=qdrant_api_key)
    
    try:
        collections = client.get_collections().collections
        print(f"\nAvailable collections: {[c.name for c in collections]}")
        
        for coll in collections:
            name = coll.name
            info = client.get_collection(collection_name=name)
            print(f"\n--- Collection: {name} ---")
            print(f"Points count: {info.points_count}")
            print(f"Vector size: {info.config.params.vectors.size if hasattr(info.config.params.vectors, 'size') else 'Multiple/Complex'}")
            
            # Get samples
            samples = client.scroll(
                collection_name=name,
                limit=3,
                with_payload=True,
                with_vectors=False
            )[0]
            
            if samples:
                print("Sample payloads:")
                for s in samples:
                    print(json.dumps(s.payload, indent=2, ensure_ascii=False))
            else:
                print("No points found in this collection.")
                
    except Exception as e:
        print(f"Error inspecting Qdrant: {e}")

if __name__ == "__main__":
    inspect_qdrant()
