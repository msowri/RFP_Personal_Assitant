from sqlalchemy import Column, Integer, String,Boolean,DateTime
from sqlalchemy.orm import relationship
from datetime import datetime
from app.db.base import Base
from app.domain.entity.domainobject import DomainObject

class User(Base,DomainObject):
    __tablename__ = "users"

    usremail    = Column(String, unique=True, index=True, nullable=False)
    usrname     = Column(String, nullable=False)
    usrpassword = Column(String, nullable=False)    
   
    # orders = relationship("Order", back_populates="user")