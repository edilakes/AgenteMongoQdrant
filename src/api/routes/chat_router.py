from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from src.core.meta_router import MetaRouter
from src.core.mcp_client import MCPClientManager
from src.core.study_librarian import StudyLibrarian
from src.core.llm_service import LLMService

router = APIRouter()

# Global singleton instances for the API
mcp_manager = MCPClientManager()
meta_router = MetaRouter(mcp_manager)
librarian = StudyLibrarian()
llm_service = LLMService()

class ChatRequest(BaseModel):
    message: str
    user_id: str = "default_user"

def clean_json(data):
    """Limpia recursivamente cualquier objeto para asegurar compatibilidad JSON."""
    if isinstance(data, dict):
        return {str(k): clean_json(v) for k, v in data.items()}
    elif isinstance(data, list):
        return [clean_json(v) for v in data]
    elif isinstance(data, (str, int, float, bool)) or data is None:
        return data
    return str(data)

@router.post("/chat")
async def chat_interaction(request: ChatRequest):
    try:
        # 1. Determinar el plan de acción (Meta-Contexto)
        plan = await meta_router.route_query(request.message)
        
        # 2. Ejecutar el plan (Recuperar información)
        context_data = await meta_router.execute_plan(plan)
        
        # 3. Estudiar el contexto y preparar la respuesta
        enriched_prompt = librarian.synthesize(
            request.message, 
            search_results=context_data if plan.get("action") == "qdrant_search" else [],
            mongo_results=context_data if plan.get("action") == "native_mongodb" else []
        )
        
        # 4. Generar respuesta final con el LLM
        answer = await llm_service.generate_response(enriched_prompt, request.message)
        
        # Brute-force JSON cleaning before returning to FastAPI
        response = {
            "intent_plan": plan,
            "answer": answer
        }
        return clean_json(response)
        
    except Exception as e:
        print(f"🔥 Error en chat_interaction: {e}")
        import traceback
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=str(e))
