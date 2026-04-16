from sqlalchemy.orm import Session
from app.repositories.document_repository import DocumentRepository
from app.services.docembedding_service  import DocEmbeddingService
from app.services.docai_service import DocAIService

class QueryService:

    def __init__(self):
        self.repo = DocumentRepository()
        self.embedder = DocEmbeddingService()
        self.ai_service = DocAIService()

    async def query(
        self,
        db: Session,
        question: str,
        top_k: int = 5,
        document_id: str = None # type: ignore
    ):
    
        query_embedding = self.embedder.generate_embedding(question) # type: ignore

        chunks = self.repo.search_similar_chunks(
            db=db,
            query_embedding=query_embedding,
            top_k=top_k,
            document_id=document_id
        )
  
        if not chunks:
            return {
                "answer": "No relevant information found.",
                "chunks": []
            }


        context = "\n\n".join(chunks)
   
        answer = await self.ai_service.ask_with_context(context, question)

        return {
            "answer": answer,
            "chunks": chunks
        }