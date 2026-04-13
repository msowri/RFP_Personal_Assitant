# from fastapi import APIRouter, Depends, HTTPException
# from pyparsing import Optional
# from sqlalchemy.orm import Session

# from app.db.session import get_db
# from app.services.query_service import QueryService
# from app.domain.schemadto.querydto import QueryRequestDto, QueryResponseDto

# router = APIRouter(prefix="/api/query", tags=["RAG Query"])

# service = QueryService()


# @router.post("/", response_model=QueryResponseDto)
# async def query_documents(
#     request: QueryRequestDto,
#     db: Session = Depends(get_db)
# ):
#     try:
#         result = await service.query(
#             db=db,
#             question=request.query,
#             top_k=request.top_k, # type: ignore
#             # document_id=request.document_id
#         )

#         return QueryResponseDto(
#             answer=request.query  ,           
#             relevant_chunks=result["chunks"]
#         )

#     except Exception as e:
#         raise HTTPException(status_code=500, detail=str(e))

