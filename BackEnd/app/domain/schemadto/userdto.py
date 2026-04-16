from pydantic import BaseModel, EmailStr   
from typing import Optional 
from  app.domain.entity.domainobject import DomainObject

class UserInputDto(BaseModel):
    id:int
    usremail: EmailStr
    usrname: Optional[str] = None
    usrpassword: str

class UserResponseDto(BaseModel,DomainObject):   
    usremail: EmailStr
    usrname: Optional[str] = None

    class Config:
        from_attributes = True   #orm mapping 


