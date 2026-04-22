from pydantic import BaseModel
from typing import Optional,List


class QueryRequestDto(BaseModel):   
    query: str
    top_k: Optional[int] = 5  # top relevant chunks 
    document_id: Optional[str] = None   
    use_aimodel: Optional[bool] = False  # Whether to use aimodel or  embeddings


class QueryResponseDto(BaseModel):   
    answer: str
    relevant_chunks: Optional[List[str]] = None     
    source_documents: Optional[List[str]] = None  