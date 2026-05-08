from sqlalchemy import Column, Integer, String, Text, ForeignKey, Boolean
from sqlalchemy.orm import relationship
from app.db.base import Base
from app.domain.entity.domainobject import DomainObject

class Question(Base, DomainObject):
    __tablename__ = "questions"

    document_id = Column(Integer, ForeignKey("documents.id"), nullable=True)
    question_text = Column(Text, nullable=False)
    normalized_text = Column(Text, nullable=True)
    is_extracted = Column(Boolean, default=True)

    document = relationship("Document", back_populates="questions")
