from groq import Groq
import os
from dotenv import load_dotenv

load_dotenv()

GROQ_API_KEY = os.getenv("GROQ_API_KEY")
AI_MODEL = os.getenv("AI_MODEL")  
print(f"GROQ_API_KEY: {GROQ_API_KEY}")  
print(f"AI_MODEL: {AI_MODEL}")  
class DocAIService:
    def __init__(self):
        self.client = Groq(api_key=GROQ_API_KEY)

    async def ask_with_context(self, context: str, question: str) -> str:
        prompt = f"""
                    You are an intelligent assistant.
                    Answer ONLY using the context below.
                    If not found, say: "Not available in document".

                    Context:
                    {context}

                    Question:
                    {question}
                    """

        response = self.client.chat.completions.create(
            model= str(AI_MODEL),  # or "mixtral-8x7b-32768", "gemma2-9b-it"
            messages=[
                {"role": "user", "content": prompt}
            ],
            temperature=0.2,
            max_tokens=1024,
        )

        return response.choices[0].message.content  # type: ignore
