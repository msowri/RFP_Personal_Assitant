from pydantic import BaseModel
from app.models.entity.domainobject import DomainObjects

class RequestDto(BaseModel):
      id:int

  