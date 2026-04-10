from sentence_transformers import SentenceTransformer
#genai installed for future use , if gemini model required for embedding
class DocEmbeddingService:
    def __init__(self):
        self.model = SentenceTransformer('all-MiniLM-L6-v2') #type : ignore ( if gemini changes will apply here)
        
    def generate_embeddings(self, texts: list[str]):
        return self.model.encode(texts).tolist() 
