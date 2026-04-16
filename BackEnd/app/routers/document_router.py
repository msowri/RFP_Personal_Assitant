from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from app.services.document_service import DocumentService
from app.db.session import get_db
import logging

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/api/documents", tags=["Documents"])
doc_service = DocumentService()


@router.get("/")
async def list_documents(
    limit: int = 10,
    offset: int = 0,
    db: Session = Depends(get_db)
):
    """List all documents"""
    try:
        documents = doc_service.get_all_documents(db, limit, offset)
        logger.info(f"test messaage")
        return {
            "success": True,
            "documents": documents,
            "total": len(documents),
            "limit": limit,
            "offset": offset
        }
    except Exception as e:
        logger.error(f"Error listing documents: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/{document_id}")
async def get_document(
    document_id: str,
    db: Session = Depends(get_db)
):
    """Get document details by ID"""
    try:
        result = doc_service.get_document(db, document_id)
        if not result:
            raise HTTPException(status_code=404, detail="Document not found")
        
        return result
    except HTTPException as e:
        raise e
    except Exception as e:
        logger.error(f"Error retrieving document: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/{document_id}/chunks")
async def get_document_chunks(
    document_id: str,
    limit: int = 10,
    offset: int = 0,
    db: Session = Depends(get_db)
):
    """Get chunks for a document"""
    try:
        chunks = doc_service.get_chunks_by_document(db, document_id, limit, offset)
        return {
            "success": True,
            "document_id": document_id,
            "chunks": chunks,
            "total": len(chunks),
            "limit": limit,
            "offset": offset
        }
    except Exception as e:
        logger.error(f"Error retrieving chunks: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))


@router.delete("/{document_id}")
async def delete_document(
    document_id: str,
    db: Session = Depends(get_db)
):
   
    try:
        result = doc_service.delete_document(db, document_id)
        return result
    except Exception as e:
        logger.error(f"Error deleting document: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))