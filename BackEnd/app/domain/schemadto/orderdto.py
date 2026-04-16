from pydantic import BaseModel, EmailStr   
from typing import Optional 
from  app.domain.entity.domainobject import DomainObject

class OrderInputDto(BaseModel,DomainObject):
    id:int    

class OrderResponseDto(BaseModel,DomainObject):   
    id:int
    user_id:int
    product: str  
    amount: float   

    class Config:
        from_attributes = True   #orm mapping 