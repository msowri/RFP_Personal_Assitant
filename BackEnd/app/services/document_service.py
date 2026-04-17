import logging
from typing import Optional, List, Dict
from sqlalchemy.orm import Session

from app.utils.text_cleaner import clean_text
from app.utils.text_chunker import chunk_sections
from app.utils.text_structurer import structure_text

from app.repositories.document_repository import DocumentRepository
from app.services.docembedding_service import DocEmbeddingService
from app.services.file_service import FileService

from app.domain.entity.documents import Document, DocumentChunk

logger = logging.getLogger(__name__)

class DocumentService:
    def __init__(self):
        self.repo = DocumentRepository()
        self.embedder = DocEmbeddingService()
        self.file_service = FileService()

    def process_and_store(
        self,
        db: Session,
        file_path: str,
        filename: str,
        file_content: Optional[bytes] = None,
        file_size: Optional[int] = None,
        chunk_size: int = 500,
        overlap: int = 50
    ) -> Dict:

        try:
           
            file_type = filename.split('.')[-1].lower()

           
            if file_content is None:
                with open(file_path, 'rb') as f:
                    file_content = f.read()

            if file_size is None:
                file_size = len(file_content)

           
            raw_text = self.file_service.extract_text(file_path)

            if not isinstance(raw_text, str) or not raw_text.strip():
                raise ValueError("No text extracted from file")

            logger.info(f"Extracted {len(raw_text)} characters from {filename}")
           
            cleaned_text = clean_text(raw_text)
          
            sections = structure_text(cleaned_text)
          
            chunks_data = chunk_sections(sections, chunk_size=chunk_size, overlap=overlap)
            if not chunks_data:
                raise ValueError("No chunks generated")
           
            chunk_texts = [c["text"] for c in chunks_data]
            logger.info(f"Generated {len(chunk_texts)} chunks")
          
            embeddings = self.embedder.generate_embeddings(chunk_texts)          
            document = Document(
                file_name=filename,
                file_type=file_type,
                file_content=file_content,
                file_size=file_size
            )
            document = self.repo.create_document(db, document)
            logger.info(f"Created document ID: {document.id}")
          
            chunk_entities = []
            for i, chunk in enumerate(chunks_data):
                chunk_entities.append(
                    DocumentChunk(
                        document_id=document.id,
                        chunk_text=chunk["text"],
                        embedding=embeddings[i],
                        chunk_index=i,
                        created_by="admin",
                        updated_by="admin",
                        is_deleted=False,
                        is_active=True
                    )
                )
           
            self.repo.bulk_insert_chunks(db, chunk_entities)
            logger.info(f"Inserted {len(chunk_entities)} chunks")
            return {
                "success": True,
                "document_id": str(document.id),
                "filename": filename,
                "file_type": file_type,
                "file_size_bytes": file_size,
                "chunks": len(chunk_entities),
                "total_characters": len(raw_text),
                "status": "Document processed successfully"
            }

        except Exception:
            logger.exception("Error processing document")
            db.rollback()
            raise

  
    def process_text_directly(
        self,
        db: Session,
        text: str,
        filename: str,
        file_type: str = "txt",
        chunk_size: int = 500,
        overlap: int = 50
    ) -> Dict:

        try:
            if not text or not text.strip():
                raise ValueError("Text cannot be empty")
            text_bytes = text.encode('utf-8')           
            cleaned_text = clean_text(text)
            sections = structure_text(cleaned_text)
            chunks_data = chunk_sections(sections, chunk_size, overlap)
            chunk_texts = [c["text"] for c in chunks_data]

            embeddings = self.embedder.generate_embeddings(chunk_texts)

            document = Document(
                file_name=filename,
                file_type=file_type,
                file_content=text_bytes,
                file_size=len(text_bytes)
            )
            document = self.repo.create_document(db, document)
            chunk_entities = []
            for i, chunk in enumerate(chunks_data):
                chunk_entities.append(
                    DocumentChunk(
                        document_id=document.id,
                        chunk_text=chunk["text"],
                        embedding=embeddings[i],
                        chunk_index=i,
                        created_by="admin",
                        updated_by="admin",
                        is_deleted=False,
                        is_active=True
                    )
                )

            self.repo.bulk_insert_chunks(db, chunk_entities)
            logger.info(f"Processed text document {document.id}")
            return {
                "success": True,
                "document_id": str(document.id),
                "chunks": len(chunk_entities)
            }

        except Exception:
            logger.exception("Error processing text")
            db.rollback()
            raise