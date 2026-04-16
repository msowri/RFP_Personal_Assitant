from pydantic import BaseModel
from typing import Optional,List


class QueryRequestDto(BaseModel):
    """DTO for query input"""
    query: str
    top_k: Optional[int] = 5  # top relevant chunks 
    use_aimodel: Optional[bool] = False  # Whether to use aimodel or  embeddings


class QueryResponseDto(BaseModel):
    """DTO for query output"""
    answer: str
    relevant_chunks: Optional[List[str]] = None     
    source_documents: Optional[List[str]] = None  