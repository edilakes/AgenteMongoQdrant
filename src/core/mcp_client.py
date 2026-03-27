import asyncio
from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client

class MCPClientManager:
    """Gestiona conexiones con múltiplos servidores MCP."""
    
    def __init__(self, config: dict = None):
        self.config = config or {}
        self.sessions = {}
        self._clients = {} # Guardar referencias a los contextos stdio

    async def start(self):
        """Inicia todas las conexiones configuradas."""
        if "mcpServers" not in self.config:
            return
            
        for name, server_config in self.config["mcpServers"].items():
            params = StdioServerParameters(
                command=server_config["command"],
                args=server_config.get("args", []),
                env=server_config.get("env")
            )
            
            # Iniciamos el cliente stdio
            client = stdio_client(params)
            read, write = await client.__aenter__()
            self._clients[name] = client
            
            session = ClientSession(read, write)
            await session.__aenter__()
            await session.initialize()
            
            self.sessions[name] = session
            print(f"✅ Conectado a MCP: {name}")

    async def list_tools(self, server_name: str):
        if server_name in self.sessions:
            return await self.sessions[server_name].list_tools()
        return None

    async def call_tool(self, server_name: str, tool_name: str, arguments: dict):
        if server_name in self.sessions:
            response = await self.sessions[server_name].call_tool(tool_name, arguments)
            if hasattr(response, 'content'):
                import json
                try:
                    return json.loads(response.content[0].text)
                except:
                    return response.content[0].text
            return response
        raise ValueError(f"Servidor {server_name} no conectado")

    async def stop(self):
        """Cierra todas las conexiones limpiamente."""
        for name, session in self.sessions.items():
            await session.__aexit__(None, None, None)
        for name, client in self._clients.items():
            await client.__aexit__(None, None, None)
        self.sessions = {}
        self._clients = {}
