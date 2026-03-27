import os
import google.generativeai as genai
from dotenv import load_dotenv

load_dotenv()

class LLMService:
    """Gestiona las llamadas al modelo de lenguaje (Gemini por defecto)."""
    
    def __init__(self):
        self.api_key = os.getenv("GEMINI_API_KEY")
        if self.api_key:
            genai.configure(api_key=self.api_key)
            self.model = genai.GenerativeModel('gemini-2.0-flash')
        else:
            self.model = None

    async def generate_response(self, system_instruction: str, user_message: str):
        if not self.model:
            return "Error: GEMINI_API_KEY no configurada en el servidor."
        
        try:
            # Combinamos la instrucción del 'Librarian' con el mensaje original
            full_prompt = f"{system_instruction}\n\nUsuario: {user_message}"
            response = self.model.generate_content(full_prompt)
            return response.text
        except Exception as e:
            return f"Error generando respuesta: {str(e)}"
