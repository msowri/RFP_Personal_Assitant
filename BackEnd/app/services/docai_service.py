import os
from dotenv import load_dotenv

load_dotenv()

AI_PROVIDER = os.getenv("AI_PROVIDER", "groq").lower()
AI_MODEL = os.getenv("AI_MODEL", "gpt-4.1-mini")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
GROQ_API_KEY = os.getenv("GROQ_API_KEY")

if AI_PROVIDER == "groq":
    from groq import Groq

if AI_PROVIDER == "openai":
    import openai
    openai.api_key = OPENAI_API_KEY

class DocAIService:
    def __init__(self):
        self.provider = AI_PROVIDER
        self.model = AI_MODEL

        if self.provider == "groq":
            if not GROQ_API_KEY:
                raise ValueError("GROQ_API_KEY is required for groq provider")
            self.client = Groq(api_key=GROQ_API_KEY)
        elif self.provider == "openai":
            if not OPENAI_API_KEY:
                raise ValueError("OPENAI_API_KEY is required for openai provider")
            self.client = openai
        else:
            raise ValueError(f"Unsupported AI provider: {self.provider}")

    async def ask_with_context(self, context: str, question: str) -> str:
        prompt = f"""
You are an intelligent assistant.
Answer only using the context below.
If not found, say: "Not available in document".

Context:
{context}

Question:
{question}
"""

        if self.provider == "groq":
            response = self.client.chat.completions.create(
                model=str(self.model),
                messages=[{"role": "user", "content": prompt}],
                temperature=0.2,
                max_tokens=1024,
            )
            return response.choices[0].message.content  # type: ignore

        if self.provider == "openai":
            completion = self.client.ChatCompletion.create(
                model=str(self.model),
                messages=[{"role": "user", "content": prompt}],
                temperature=0.2,
                max_tokens=1024,
            )
            return completion.choices[0].message["content"].strip()

        raise ValueError(f"Cannot process AI request for provider {self.provider}")
