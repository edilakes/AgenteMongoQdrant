import sys
import os

# Para poder importar src
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.core.meta_router import MetaRouter
from src.core.mcp_client import MCPClientManager
import asyncio
from dotenv import load_dotenv

load_dotenv()

async def test_meta_routing():
    print("--- Probando Estrategia de Meta-Contexto ---")
    mcp_manager = MCPClientManager()
    router = MetaRouter(mcp_manager)
    
    # Query que debería ir a MongoDB
    query_norma = "¿Qué dice la norma sobre el tiempo de estudio?"
    plan_norma = await router.route_query(query_norma)
    print(f"\nQuery: {query_norma}")
    print(f"Plan decidido: {plan_norma}")
    
    # Query que debería ir a Qdrant
    query_doctrina = "Resumen sobre la humildad en Escriva"
    plan_doctrina = await router.route_query(query_doctrina)
    print(f"\nQuery: {query_doctrina}")
    print(f"Plan decidido: {plan_doctrina}")

if __name__ == "__main__":
    asyncio.run(test_meta_routing())
