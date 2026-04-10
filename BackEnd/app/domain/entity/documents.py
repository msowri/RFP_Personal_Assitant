from sqlalchemy import Column, ForeignKey, Integer, String,Boolean,DateTime
from sqlalchemy.orm import relationship
from datetime import datetime
from pgvector.sqlalchemy import Vector

from app.db.base import Base
from app.domain.entity.domainobject import DomainObject


class Document(Base,DomainObject ):
    __tablename__ = "documents"
   
    file_name = Column(String)
    file_type = Column(String)    

class DocumentChunk(Base,DomainObject):
    __tablename__ = "document_chunks"

    # document_id = Column(Integer), ForeignKey("documents.id"))
    chunk_text = Column(String)
    embedding = Column(Vector(768))  # adjust dimension(gemini)/adjustment required for groq
    chunk_index = Column(Integer)
    # document_id = Column(Integer)
    chunk_index = Column(Integer)
    chunk_text = Column(String)