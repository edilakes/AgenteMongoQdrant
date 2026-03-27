class StudyLibrarian:
    """
    Habilidad especializada para estudiar el contexto recuperado 
    y generar una síntesis coherente con citas textuales.
    """
    
    def __init__(self):
        pass

    def synthesize(self, prompt: str, search_results: list, mongo_results: list = None):
        """
        Combina los resultados de Qdrant y MongoDB para crear 
        un contexto rico para el LLM.
        """
        context_parts = []
        
        if search_results:
            context_parts.append("### Información Doctrinaria (Qdrant):")
            for i, res in enumerate(search_results):
                # Manejar diferentes formatos de resultado de Qdrant
                text = getattr(res, 'document', str(res))
                context_parts.append(f"[{i+1}] {text}")
        
        if mongo_results:
            context_parts.append("\n### Información Detallada (MongoDB):")
            for i, res in enumerate(mongo_results):
                context_parts.append(f"- {str(res)}")
        
        system_prompt = (
            "Eres un agente experto con acceso a una biblioteca extensa. "
            "Tu tarea es estudiar el contexto proporcionado y responder con precisión. "
            "Si encuentras una cita textual relevante, inclúyela entre comillas.\n\n"
            f"Contexto:\n{' '.join(context_parts)}\n\n"
            f"Pregunta del usuario: {prompt}"
        )
        
        return system_prompt
