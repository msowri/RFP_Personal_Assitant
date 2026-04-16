# from google import genai                       
# import os
# from dotenv import load_dotenv

# load_dotenv()
# GEMINI_API_KEY = os.getenv("GEMINI_API_KEY") #expired issue in Gemini API key, need to check and update
# GROQ_API_KEY = os.getenv("GROQ_API_KEY")

# class DocAIService:
#     def __init__(self):
#         self.client = genai.Client(api_key=GEMINI_API_KEY)  # 

#     async def ask_with_context(self, context: str, question: str) -> str:
#         prompt = f"""
#                     You are an intelligent assistant.
#                     Answer ONLY using the context below.
#                     If not found, say: "Not available in document".

#                     Context:
#                     {context}

#                     Question:
#                     {question}
#                     """
#         response = await self.client.aio.models.generate_content(
#             model="gemini-2.0-flash",          
#             contents=prompt
#         )
#         return response.text # type: ignore