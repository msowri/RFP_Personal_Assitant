import logging
import warnings
from sentence_transformers import SentenceTransformer
from typing import List

# Suppress HuggingFace warnings
logging.getLogger("transformers").setLevel(logging.ERROR)
logging.getLogger("huggingface_hub").setLevel(logging.ERROR)
warnings.filterwarnings("ignore")


class DocEmbeddingService:
    def __init__(self):
        """Initialize embedding service with sentence transformer model"""
        #self.model = SentenceTransformer('all-MiniLM-L6-v2') #384
        self.model = SentenceTransformer("all-mpnet-base-v2") #768
        

    def generate_embedding(self, text: str) -> List[float]:
        return self.model.encode(text).tolist()
        
    def generate_embeddings(self, texts: List[str]) -> List[List[float]]:
        return self.model.encode(texts).tolist()
