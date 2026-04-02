import os
import asyncio
from pymongo import MongoClient
from qdrant_client import QdrantClient
import google.generativeai as genai
from dotenv import load_dotenv

async def test_mongodb():
    print("--- Testing MongoDB ---")
    mongo_url = os.getenv("MONGO_URL")
    try:
        client = MongoClient(mongo_url, serverSelectionTimeoutMS=5000)
        client.admin.command('ping')
        print("✅ MongoDB connection successful!")
        return True
    except Exception as e:
        print(f"❌ MongoDB connection failed: {e}")
        return False

async def test_qdrant():
    print("\n--- Testing Qdrant ---")
    qdrant_url = os.getenv("QDRANT_URL")
    qdrant_api_key = os.getenv("QDRANT_API_KEY")
    try:
        client = QdrantClient(url=qdrant_url, api_key=qdrant_api_key)
        # Try to list collections as a simple ping
        client.get_collections()
        print("✅ Qdrant connection successful!")
        return True
    except Exception as e:
        print(f"❌ Qdrant connection failed: {e}")
        return False

async def test_gemini():
    print("\n--- Testing Gemini ---")
    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key:
        print("❌ Gemini API Key not found in .env")
        return False
    
    try:
        genai.configure(api_key=api_key)
        model = genai.GenerativeModel('gemini-2.0-flash')
        response = model.generate_content("Responde 'OK' si recibes esto.")
        print(f"✅ Gemini response: {response.text.strip()}")
        return True
    except Exception as e:
        print(f"❌ Gemini test failed: {e}")
        return False

async def main():
    load_dotenv()
    print("Starting connection tests...")
    
    results = await asyncio.gather(
        test_mongodb(),
        test_qdrant(),
        test_gemini()
    )
    
    print("\n--- Final Results ---")
    if all(results):
        print("🚀 All connections are working correctly!")
    else:
        print("⚠️ Some connections failed. Please check the logs above.")

if __name__ == "__main__":
    asyncio.run(main())
