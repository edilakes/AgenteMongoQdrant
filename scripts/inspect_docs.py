import os
from pymongo import MongoClient
from dotenv import load_dotenv
import json
from bson import json_util

def inspect_docs():
    load_dotenv()
    mongo_url = os.getenv("MONGO_URL")
    client = MongoClient(mongo_url)
    
    targets = [
        ("OposicionesDB", "normas"),
        ("OposicionesDB", "preguntas"),
        ("EscrivaRAG", "chunks"),
        ("itheca", "knowledge_base")
    ]
    
    for db_name, coll_name in targets:
        print(f"\n--- Sample from {db_name}.{coll_name} ---")
        db = client[db_name]
        doc = db[coll_name].find_one()
        if doc:
            print(json.dumps(doc, indent=2, default=json_util.default, ensure_ascii=False))
        else:
            print("No documents found.")

if __name__ == "__main__":
    inspect_docs()
