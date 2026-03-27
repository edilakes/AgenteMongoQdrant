import asyncio
import os
from dotenv import load_dotenv
from src.core.semantic_indexer import SemanticIndexer
from src.core.mcp_client import MCPClientManager

async def run_indexing():
    load_dotenv()
    
    # Necesitamos el manager para hablar con las fuentes
    mcp_config = {
        "mcpServers": {
            "mongodb": {
                "command": "npx",
                "args": ["-y", "@modelcontextprotocol/server-mongodb", os.getenv("MONGO_URL")]
            }
        }
    }
    
    indexer = SemanticIndexer()
    
    try:
        # Indexamos las Normas
        await indexer.index_mongodb_collection(
            db_name="OposicionesDB",
            collection_name="normas"
        )
        # Indexamos la Biblia
        await indexer.index_mongodb_collection(
            db_name="Pioteca",
            collection_name="Biblia"
        )
    finally:
        pass

if __name__ == "__main__":
    asyncio.run(run_indexing())
