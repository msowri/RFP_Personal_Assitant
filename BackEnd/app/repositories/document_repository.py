from typing import Optional
from sqlalchemy.orm import Session
from sqlalchemy import text
from app.domain.entity.documents import Document, DocumentChunk

class DocumentRepository:

    def create_document(self, db: Session, doc: Document):        
        db.add(doc)
        db.commit()
        db.refresh(doc)
        return doc

    def bulk_insert_chunks(self, db: Session, chunks: list[DocumentChunk]):        
        db.bulk_save_objects(chunks)
        db.commit()

    def get_document(self, db: Session, document_id):       
        try:
            return db.query(Document).filter(Document.id == document_id).first()
        except Exception as e:
            raise e

    def get_document_with_content(self, db: Session, document_id):       
        try:
            return db.query(Document).filter(Document.id == document_id).first()
        except Exception as e:
            raise e

    def get_chunks_by_document(self, db: Session, document_id, limit: int = 10, offset: int = 0):        
        try:
            return db.query(DocumentChunk).filter(
                DocumentChunk.document_id == document_id
            ).limit(limit).offset(offset).all()
        except Exception as e:
            raise e

    def get_all_documents(self, db: Session, limit: int = 10, offset: int = 0):         # future list use only added
        try:
            return db.query(Document).limit(limit).offset(offset).all()
        except Exception as e:
            raise e

    def get_chunks_count(self, db: Session, document_id):        
        try:
            return db.query(DocumentChunk).filter(
                DocumentChunk.document_id == document_id
            ).count()
        except Exception as e:
            raise e

    def delete_document(self, db: Session, document_id):        
        try:
            doc = db.query(Document).filter(Document.id == document_id).first()
            if doc:
                db.delete(doc)
                db.commit()
                return True
            return False
        except Exception as e:
            db.rollback()
            raise e

    def delete_chunks_by_document(self, db: Session, document_id):       
        try:
            count = db.query(DocumentChunk).filter(
                DocumentChunk.document_id == document_id
            ).delete()
            db.commit()
            return count
        except Exception as e:
            db.rollback()
            raise e

    def get_document_file_metadata(self, db: Session, document_id):       
        try:
            doc = db.query(Document).filter(Document.id == document_id).first()
            if not doc:
                return None
            
            return {
                "id": doc.id,
                "file_name": doc.file_name,
                "file_type": doc.file_type,
                "file_size": doc.file_size,
                "created_on": doc.created_on,
                "updated_on": doc.updated_on,
                "has_content": doc.file_content is not None
            }
        except Exception as e:
            raise e
        


    def search_similar_chunks(
        self,
        db: Session,
        query_embedding: list,
        top_k: int = 5,
        document_id: Optional[str] = None
    ):
        sql = """
        SELECT chunk_text
        FROM document_chunks
        WHERE (:document_id IS NULL OR document_id = :document_id)
        ORDER BY embedding <-> CAST(:embedding AS vector)
        LIMIT :top_k
        """

        result = db.execute(
            text(sql),
            {
                "embedding": query_embedding,
                "top_k": top_k,
                "document_id": document_id
            }
        )

        return [row[0] for row in result.fetchall()]
       

                            