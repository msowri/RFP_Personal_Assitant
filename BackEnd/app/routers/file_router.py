from fastapi import APIRouter, UploadFile, File, HTTPException, Depends
from sqlalchemy.orm import Session
from app.services.file_service import FileService
from app.services.document_service import DocumentService
from app.db.session import get_db
import logging

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/api/files", tags=["Files"])
file_service = FileService()
doc_service = DocumentService()


@router.post("/upload")
async def upload_file(
    file: UploadFile = File(...),
    db: Session = Depends(get_db)
):
    """
    Upload and process a file
    - Supports: PDF, TXT, DOCX
    - Max size: 50MB
    """
    try:
        #read
        file_content = await file.read()
        
       
        is_valid, message = file_service.validate_file(file.filename, len(file_content)) # type: ignore
        if not is_valid:
            raise HTTPException(status_code=400, detail=message)
        
        # Save 
        file_metadata = file_service.save_file(file_content, file.filename) # type: ignore
        
        # Extract 
        extracted_text = file_service.extract_text(file_metadata["file_path"])
        
        #  store in DB
        doc_result = doc_service.process_and_store(
            db, 
            file_metadata["file_path"],
            file.filename # type: ignore
        )
        
        return {
            "success": True,
            "file_id": file_metadata["file_id"],
            "file_name": file_metadata["original_name"],
            "file_size_mb": round(file_metadata["size_bytes"] / (1024 * 1024), 2),
            "file_type": file_metadata["file_type"],
            "document_id": doc_result["document_id"],
            "chunks_created": doc_result["chunks"],
            "total_characters": doc_result["total_characters"]
        }
    
    except HTTPException as e:
        raise e
    except Exception as e:
        logger.error(f"File upload error: {str(e)}")
        raise HTTPException(status_code=500, detail=f"File upload failed: {str(e)}")


@router.post("/extract-text")
async def extract_text_only(file: UploadFile = File(...)):
    """
    Extract text from uploaded file without storing in database
    """
    try:
        file_content = await file.read()
        
        # Validate file
        is_valid, message = file_service.validate_file(file.filename, len(file_content)) # type: ignore
        if not is_valid:
            raise HTTPException(status_code=400, detail=message)
        
        # temp save
        file_metadata = file_service.save_file(file_content, file.filename) # type: ignore
        
        # Extract text
        extracted_text = file_service.extract_text(file_metadata["file_path"])
        
        return {
            "success": True,
            "file_name": file_metadata["original_name"],
            "file_type": file_metadata["file_type"],
            "file_size_mb": round(file_metadata["size_bytes"] / (1024 * 1024), 2),
            "characters_extracted": len(extracted_text),
            "text": extracted_text
        }
    
    except HTTPException as e:
        raise e
    except Exception as e:
        logger.error(f"Text extraction error: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Text extraction failed: {str(e)}")


@router.get("/validate/{filename}/{file_size}")
async def validate_file_endpoint(filename: str, file_size: int):
    """
    Validate file before upload
    
    Args:
        filename: Name of the file
        file_size: Size in bytes
    """
    is_valid, message = file_service.validate_file(filename, file_size)
    return {
        "valid": is_valid,
        "message": message,
        "filename": filename,
        "file_size_mb": round(file_size / (1024 * 1024), 2), #changes required
        "max_allowed_mb": 50, #changes required
        "allowed_types": ["pdf", "txt", "docx"] #changes required
    }


@router.get("/info")
async def file_settings_info():
    """Get file upload settings"""
    return {
        "max_file_size_mb": 50,
        "allowed_file_types": ["pdf", "txt", "docx"],
        "upload_directory": "uploads/"
    }