from sqlalchemy.orm import Session
from app.domain.entity.documents import Document, DocumentChunk

class DocumentRepository:

    def create_document(self, db: Session, doc: Document): #relationship & validation pending for document and document chunk
        db.add(doc)
        db.commit()
        db.refresh(doc)
        return doc

    def bulk_insert_chunks(self, db: Session, chunks: list[DocumentChunk]): #relationship & validation pending for document and document chunk
        db.bulk_save_objects(chunks)
        db.commit()