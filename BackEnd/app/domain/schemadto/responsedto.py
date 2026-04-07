from pydantic import BaseModel
from  app.domain.entity.domainobject import DomainObject

class ResponseDto(BaseModel,DomainObject):
    id:int
    class Config:
        from_attributes = True   #orm mapping 