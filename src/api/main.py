import os
from fastapi import FastAPI
from src.api.routes import chat_router

# Simplificamos main.py para evitar problemas de lifespan con procesos bloqueantes
app = FastAPI(title="Agente Universal MCP - Pure Context Edition")

@app.get("/")
async def root():
    return {"message": "Agente Universal MCP operativo (Adaptador Nativo)"}

app.include_router(chat_router.router, prefix="/api/v1")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
