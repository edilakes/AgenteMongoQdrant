import os
from pymongo import MongoClient
from dotenv import load_dotenv

def inspect_mongodb():
    load_dotenv()
    mongo_url = os.getenv("MONGO_URL")
    print(f"Connecting to MongoDB...")
    client = MongoClient(mongo_url)
    
    try:
        dbs = client.list_database_names()
        print(f"\nDatabases: {dbs}")
        
        for db_name in dbs:
            if db_name in ['admin', 'config', 'local']:
                continue
            print(f"\n--- Database: {db_name} ---")
            db = client[db_name]
            colls = db.list_collection_names()
            for coll_name in colls:
                count = db[coll_name].count_documents({})
                print(f" - {coll_name}: {count} documents")
                
    except Exception as e:
        print(f"Error inspecting MongoDB: {e}")

if __name__ == "__main__":
    inspect_mongodb()
