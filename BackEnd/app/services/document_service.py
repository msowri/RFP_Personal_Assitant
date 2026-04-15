import uuid
from sqlalchemy.orm import Session
from app.repositories.document_repository import DocumentRepository
from app.services.docembedding_service import DocEmbeddingService
from app.utils.text_chunker import chunk_text
from app.domain.entity.documents import Document, DocumentChunk

class DocumentService:
    def __init__(self):
        self.repo = DocumentRepository()   #variable created for class objec ref
        self.embedder = DocEmbeddingService()        

    def process_and_store(self, db: Session, file_content: bytes, filename: str):       
        metadata = ""     #file service required
        text =   "Test"  
        chunks = chunk_text(text)      
        embeddings = self.embedder.generate_embeddings(chunks)        
        document = Document(
            file_name=filename,
            # file_type=metadata["file_type"]
        )
        document = self.repo.create_document(db, document)       
        chunk_entities = []
        for i, chunk in enumerate(chunks):
            chunk_entities.append(
                DocumentChunk(
                    document_id=document.id,
                    chunk_text=chunk,
                    embedding=embeddings[i],
                    chunk_index=i
                )
            )

        self.repo.bulk_insert_chunks(db, chunk_entities)
        return {
            "document_id": str(document.id),
            "chunks": len(chunks)
        }