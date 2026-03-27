import os
from src.core.mcp_client import MCPClientManager
from dotenv import load_dotenv

load_dotenv()

async def setup_agent_tools():
    """Configura los servidores MCP para el agente."""
    manager = MCPClientManager()
    remote_ip = os.getenv("REMOTE_IP")
    mongo_url = os.getenv("MONGO_URL")

    # 1. Conectar a MCP MongoDB (Asumiendo que el servidor MCP se ejecuta localmente o vía Docker proxy)
    # Para desarrollo, podemos usar npx directamente si está disponible
    # O simplemente preparar el comando que el núcleo usará.
    
    # Ejemplo de configuración para el gestor:
    # mcp_mongodb_cmd = f"npx @mongodb-js/mongodb-mcp-server --mongodbUrl={mongo_url}"
    # await manager.connect_to_server("mongodb", "npx", ["@mongodb-js/mongodb-mcp-server", "--mongodbUrl", mongo_url])
    
    # 2. Conectar a MCP Qdrant
    # qdrant_url = os.getenv("QDRANT_URL")
    # await manager.connect_to_server("qdrant", "qdrant-mcp-server", env={"QDRANT_URL": qdrant_url})
    
    return manager

# Esta es la base para la Fase 3: Orquestación
