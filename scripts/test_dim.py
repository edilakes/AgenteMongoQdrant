import os
import google.generativeai as genai
from dotenv import load_dotenv

def test_embedding_dim():
    load_dotenv()
    api_key = os.getenv("GEMINI_API_KEY")
    genai.configure(api_key=api_key)
    
    model = "models/gemini-embedding-001"
    text = "Hola mundo"
    
    result = genai.embed_content(
        model=model,
        content=text,
        task_type="retrieval_document"
    )
    embedding = result['embedding']
    print(f"Model: {model}")
    print(f"Dimension: {len(embedding)}")

if __name__ == "__main__":
    test_embedding_dim()
