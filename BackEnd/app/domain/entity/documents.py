from sqlalchemy import Column, ForeignKey, Integer, String, LargeBinary
from sqlalchemy.orm import relationship
from pgvector.sqlalchemy import Vector

from app.db.base import Base
from app.domain.entity.domainobject import DomainObject


class Document(Base, DomainObject):
   
    __tablename__ = "documents"
    
    file_name = Column(String, nullable=False)
    file_type = Column(String, nullable=False)
    file_content = Column(LargeBinary, nullable=True)  # Embedded file content
    file_size = Column(Integer, nullable=True)  # File size in bytes
    
    # Relationship to document chunks
    chunks = relationship("DocumentChunk", back_populates="document", cascade="all, delete-orphan")


class DocumentChunk(Base, DomainObject):
    
    __tablename__ = "document_chunks"
    
    document_id = Column(Integer, ForeignKey("documents.id"), nullable=False)
    chunk_text = Column(String, nullable=False)
    #embedding = Column(Vector(384))  # MiniLM-L6-v2 produces 384-dimensional embeddings
    embedding = Column(Vector(768))  # Gemini
    chunk_index = Column(Integer, nullable=False)
    
    # Relationship back to document
    document = relationship("Document", back_populates="chunks")