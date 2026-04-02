import asyncio
import os
from src.core.semantic_indexer import SemanticIndexer
from dotenv import load_dotenv

async def main():
    load_dotenv()
    indexer = SemanticIndexer()
    
    # 1. Recrear colecciones
    print("Recreando colecciones en Qdrant...")
    indexer.recreate_collection("context_map", 3072)
    indexer.recreate_collection("doctrina_itheca", 3072)
    
    # 2. Indexación de OposicionesDB.normas -> context_map
    # Limitamos para este primer proceso de prueba real, o quitamos el límite para completo
    # Vamos a procesar un número razonable para validar
    await indexer.index_mongodb_collection(
        db_name="OposicionesDB", 
        collection_name="normas", 
        qdrant_collection="context_map"
    )
    
    # 3. Indexación de OposicionesDB.preguntas -> context_map
    await indexer.index_mongodb_collection(
        db_name="OposicionesDB", 
        collection_name="preguntas", 
        qdrant_collection="context_map",
        limit=500 # Limitamos preguntas para no saturar la API en la primera pasada
    )
    
    # 4. Indexación de itheca.knowledge_base -> doctrina_itheca
    await indexer.index_mongodb_collection(
        db_name="itheca", 
        collection_name="knowledge_base", 
        qdrant_collection="doctrina_itheca",
        limit=500
    )
    
    # 5. Indexación de EscrivaRAG.chunks -> doctrina_itheca
    await indexer.index_mongodb_collection(
        db_name="EscrivaRAG", 
        collection_name="chunks", 
        qdrant_collection="doctrina_itheca",
        limit=500
    )

    print("\n🚀 Re-indexación finalizada con éxito.")

if __name__ == "__main__":
    asyncio.run(main())
