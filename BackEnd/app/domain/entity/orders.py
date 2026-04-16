# app/models/order.py
from sqlalchemy import Column, Integer, String, Float, ForeignKey
# from sqlalchemy.orm import relationship - for feature use added
from app.db.base import Base
from app.domain.entity.domainobject import DomainObject

class Order(Base,DomainObject):
    __tablename__ = "orders"   

    user_id  = Column(Integer, ForeignKey("users.id"))
    product  = Column(String)
    amount   = Column(Float)

    # user = relationship("User", back_populates="orders")