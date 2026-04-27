from pydantic import BaseModel
from typing import Optional
from datetime import datetime
 


class DraftCreate(BaseModel):
    question: str
    answer: str
    document_id: Optional[int] = None  

class DraftUpdate(BaseModel):
    question: Optional[str] = None
    answer: Optional[str] = None
    document_id: Optional[int] = None
    is_edited: Optional[bool] = None  


class DraftResponse(BaseModel):
    id: int
    question: str
    answer: str
    document_id: Optional[int] = None
    is_edited: bool
    created_at: datetime
    updated_at: datetime

    # class Config:
    #     orm_mode = True
