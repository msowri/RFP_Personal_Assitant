import logging
from typing import Optional, List, Dict
from sqlalchemy import text
from sqlalchemy.orm import Session
from app.repositories.document_repository import DocumentRepository
from app.services.docembedding_service import DocEmbeddingService
from app.services.file_service import FileService
from app.utils.text_chunker import chunk_text
from app.domain.entity.documents import Document, DocumentChunk

logger = logging.getLogger(__name__)


class DocumentService:
    def __init__(self):
        """Initialize DocumentService with required dependencies"""
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
        """
        Process file and store document with embeddings and embedded file content
        
        Args:
            db: Database session
            file_path: Path to the saved file
            filename: Original filename
            file_content: Binary content of the file (optional)
            file_size: Size of the file in bytes (optional)
            chunk_size: Size of text chunks (default 500)
            overlap: Overlap between chunks (default 50)
        
        Returns:
            Dict with document_id, filename, file_type, chunks count, total characters, file_size
        """
        try:
            # Extract 
            file_type = filename.split('.')[-1].lower()
            
           
            if file_content is None:
                with open(file_path, 'rb') as f:
                    file_content = f.read()
            
           
            if file_size is None:
                file_size = len(file_content)
            
           
            text = self.file_service.extract_text(file_path)
            
            if not text or len(text.strip()) == 0:
                raise ValueError("No text extracted from file")
            
            logger.info(f"Extracted {len(text)} characters from {filename}")
            
            #  into chunks
            chunks = chunk_text(text, chunk_size=chunk_size, overlap=overlap)
            
            if not chunks:
                raise ValueError("No chunks generated from text")
            
            logger.info(f"Generated {len(chunks)} chunks from {filename}")
            
            #  embeddings for all chunks
            embeddings = self.embedder.generate_embeddings(chunks)
            
            #  embedded file content
            document = Document(
                file_name=filename,
                file_type=file_type,
                file_content=file_content,
                file_size=file_size
            )
            document = self.repo.create_document(db, document)
            logger.info(f"Created document with ID: {document.id}, size: {file_size} bytes")
            
         
            chunk_entities = []
            for i, chunk in enumerate(chunks):
                chunk_entity = DocumentChunk(
                    document_id=document.id,
                    chunk_text=chunk,
                    embedding=embeddings[i],
                    chunk_index=i,
                    created_by="admin",
                    updated_by="admin",
                    is_deleted=False,
                    is_active=True
                )
                chunk_entities.append(chunk_entity)
            
            # Bulk insert chunks
            self.repo.bulk_insert_chunks(db, chunk_entities)
            logger.info(f"Inserted {len(chunk_entities)} chunks for document {document.id}")
            
            return {
                "success": True,
                "document_id": str(document.id),
                "filename": filename,
                "file_type": file_type,
                "file_size_bytes": file_size,
                "chunks": len(chunks),
                "total_characters": len(text),
                "status": "Document processed and stored successfully with embedded content"
            }
        
        except ValueError as ve:
            logger.error(f"Validation error: {str(ve)}")
            db.rollback()
            raise
        except Exception as e:
            logger.error(f"Error processing document: {str(e)}")
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
        """
        Process raw text and store document with embeddings and embedded content
        Useful for processing text without a physical file
        
        Args:
            db: Database session
            text: Raw text to process
            filename: Document filename
            file_type: File type (default: txt)
            chunk_size: Size of text chunks
            overlap: Overlap between chunks
        
        Returns:
            Dict with document_id and chunks count
        """
        try:
            if not text or len(text.strip()) == 0:
                raise ValueError("Text cannot be empty")
            
          
            text_bytes = text.encode('utf-8')
            
          
            chunks = chunk_text(text, chunk_size=chunk_size, overlap=overlap)
            
            if not chunks:
                raise ValueError("No chunks generated from text")
            
           
            embeddings = self.embedder.generate_embeddings(chunks)
            
           
            document = Document(
                file_name=filename,
                file_type=file_type,
                file_content=text_bytes,
                file_size=len(text_bytes)
            )
            document = self.repo.create_document(db, document)
            
          
            chunk_entities = []
            for i, chunk in enumerate(chunks):
                chunk_entity = DocumentChunk(
                    document_id=document.id,
                    chunk_text=chunk,
                    embedding=embeddings[i],
                    chunk_index=i,
                    created_by="admin",
                    updated_by="admin",
                    is_deleted=False,
                    is_active=True
                )
                chunk_entities.append(chunk_entity)
            
           
            self.repo.bulk_insert_chunks(db, chunk_entities)
            
            logger.info(f"Processed text document {document.id} with {len(chunks)} chunks, size: {len(text_bytes)} bytes")
            
            return {
                "success": True,
                "document_id": str(document.id),
                "filename": filename,
                "file_type": file_type,
                "file_size_bytes": len(text_bytes),
                "chunks": len(chunks),
                "total_characters": len(text),
                "status": "Text processed and stored successfully with embedded content"
            }
        
        except Exception as e:
            logger.error(f"Error processing text: {str(e)}")
            db.rollback()
            raise

    def get_document(self, db: Session, document_id: str) -> Optional[Dict]:
        """Retrieve document by ID with embedded metadata"""
        try:
            document = self.repo.get_document(db, document_id)
            if not document:
                return None
            
         
            chunks_count = self.repo.get_chunks_count(db, document_id)
            
            return {
                "success": True,
                "document_id": str(document.id),
                "filename": document.file_name,
                "file_type": document.file_type,
                "file_size_bytes": document.file_size,
                "created_on": document.created_on.isoformat() if document.created_on else None,  # type: ignore
                "updated_on": document.updated_on.isoformat() if document.updated_on else None,  # type: ignore
                "chunks_count": chunks_count,
                "has_embedded_content": document.file_content is not None
            }
        except Exception as e:
            logger.error(f"Error retrieving document: {str(e)}")
            raise

    def get_chunks_by_document(
        self, 
        db: Session, 
        document_id: str,
        limit: int = 10,
        offset: int = 0
    ) -> List[Dict]:
        """Retrieve chunks for a document with pagination"""
        try:
            chunks = self.repo.get_chunks_by_document(db, document_id, limit, offset)
            
            result = []
            for i, chunk in enumerate(chunks):
                text_content = chunk.chunk_text if chunk.chunk_text else "" # type: ignore
                text_preview = (text_content[:100] + "...") if text_content and len(text_content) > 100 else text_content # type: ignore
                
                result.append({
                    "chunk_id": i,
                    "chunk_index": chunk.chunk_index,
                    "text": text_content,
                    "text_preview": text_preview
                })
            
            return result
        except Exception as e:
            logger.error(f"Error retrieving chunks: {str(e)}")
            raise

    def delete_document(self, db: Session, document_id: str) -> Dict:
        """
        Delete document and its chunks
        
        Args:
            db: Database session
            document_id: Document ID to delete
        
        Returns:
            Deletion status
        """
        try:
         
            chunks_deleted = self.repo.delete_chunks_by_document(db, document_id)
            
          
            document_deleted = self.repo.delete_document(db, document_id)
            
            logger.info(f"Deleted document {document_id} with {chunks_deleted} chunks")
            
            return {
                "success": True,
                "document_id": document_id,
                "document_deleted": document_deleted,
                "chunks_deleted": chunks_deleted,
                "status": "Document deleted successfully"
            }
        except Exception as e:
            logger.error(f"Error deleting document: {str(e)}")
            db.rollback()
            raise

    def get_all_documents(self, db: Session, limit: int = 10, offset: int = 0) -> List[Dict]:
        """
        Retrieve all documents with pagination
        
        Args:
            db: Database session
            limit: Number of documents to return
            offset: Pagination offset
        
        Returns:
            List of documents with their metadata
        """
        try:
            documents = self.repo.get_all_documents(db, limit, offset)
            
            result = []
            for doc in documents:
                chunks_count = self.repo.get_chunks_count(db, str(doc.id))
                
                result.append({
                    "document_id": str(doc.id),
                    "filename": doc.file_name,
                    "file_type": doc.file_type,
                    "chunks_count": chunks_count
                })
            
            logger.info(f"Retrieved {len(result)} documents")
            return result
        except Exception as e:
            logger.error(f"Error retrieving documents: {str(e)}")
            raise

# ##################################Query######################################################
