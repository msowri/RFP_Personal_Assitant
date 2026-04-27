from sqlalchemy import Column , Integer,String , LargeBinary, ForeignKey, Boolean
from sqlalchemy.orm import relationship
from .domainobject import DomainObject
from app.db.base import Base

class Draft(Base,DomainObject):
    __tablename__ = "drafts"
    
    question = Column(String, nullable=True)   
    answer  = Column(String, nullable=True)
    document_id = Column(Integer, ForeignKey("documents.id"), nullable=True)
    is_edited   = Column(Boolean, default=False)  # Indicates if the draft has been edited

   # Relationship back to document
    document = relationship("Document", back_populates="chunks")  