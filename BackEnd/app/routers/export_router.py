from fastapi import APIRouter, HTTPException, Depends, Response
from sqlalchemy.orm import Session
from app.services.export_service import ExportService
from app.services.draft_service import DraftService
from app.services.document_service import DocumentService
from app.db.session import get_db
from pydantic import BaseModel
from typing import List, Optional
import logging

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/api/export", tags=["Export"])
export_service = ExportService()
draft_service = DraftService()
doc_service = DocumentService()

class ExportRequest(BaseModel):
    document_id: Optional[int] = None
    draft_ids: Optional[List[int]] = None
    format: str = "docx"  # docx, txt
    include_metadata: bool = True

class QAExportRequest(BaseModel):
    qa_pairs: List[dict]
    title: Optional[str] = None
    format: str = "docx"
    metadata: Optional[dict] = None

@router.post("/drafts")
async def export_drafts(
    request: ExportRequest,
    db: Session = Depends(get_db)
):
    """Export drafts to specified format"""
    try:
        if request.format not in ["docx", "txt"]:
            raise HTTPException(status_code=400, detail="Unsupported format. Use 'docx' or 'txt'")
        
        # Get drafts to export
        if request.draft_ids:
            drafts = []
            for draft_id in request.draft_ids:
                draft = draft_service.get_draft(db, draft_id)
                if draft:
                    drafts.append({
                        'id': draft.id,
                        'question': draft.question,
                        'answer': draft.answer,
                        'is_edited': draft.is_edited,
                        'created_on': str(draft.created_on),
                        'updated_on': str(draft.updated_on)
                    })
        elif request.document_id:
            # Get all drafts for a document
            # Note: You'll need to implement this method in draft_service
            drafts = draft_service.get_drafts_by_document(db, request.document_id)
        else:
            raise HTTPException(status_code=400, detail="Either draft_ids or document_id must be provided")
        
        if not drafts:
            raise HTTPException(status_code=404, detail="No drafts found to export")
        
        # Get document info if available
        document_info = None
        if request.document_id and request.include_metadata:
            document = doc_service.get_document(db, request.document_id)
            if document:
                document_info = {
                    'file_name': document.file_name,
                    'file_type': document.file_type,
                    'created_on': str(document.created_on)
                }
        
        # Export based on format
        if request.format == "docx":
            docx_buffer = export_service.export_drafts_to_docx(drafts, document_info)
            
            return Response(
                content=docx_buffer.getvalue(),
                media_type="application/vnd.openxmlformats-officedocument.wordprocessingml.document",
                headers={"Content-Disposition": "attachment; filename=rfp_drafts.docx"}
            )
        else:  # txt
            content = {
                'title': 'RFP Response Drafts',
                'metadata': document_info,
                'qa_pairs': drafts,
                'additional_content': []
            }
            text_content = export_service.export_to_text(content)
            
            return Response(
                content=text_content,
                media_type="text/plain",
                headers={"Content-Disposition": "attachment; filename=rfp_drafts.txt"}
            )
        
    except HTTPException as e:
        raise e
    except Exception as e:
        logger.error(f"Error exporting drafts: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Export failed: {str(e)}")

@router.post("/qa")
async def export_qa_pairs(
    request: QAExportRequest,
    db: Session = Depends(get_db)
):
    """Export Q&A pairs to specified format"""
    try:
        if request.format not in ["docx", "txt"]:
            raise HTTPException(status_code=400, detail="Unsupported format. Use 'docx' or 'txt'")
        
        if not request.qa_pairs:
            raise HTTPException(status_code=400, detail="No Q&A pairs provided")
        
        content = {
            'title': request.title or 'RFP Q&A Document',
            'metadata': request.metadata or {},
            'qa_pairs': request.qa_pairs,
            'additional_content': []
        }
        
        if request.format == "docx":
            docx_buffer = export_service.export_to_docx(content)
            
            return Response(
                content=docx_buffer.getvalue(),
                media_type="application/vnd.openxmlformats-officedocument.wordprocessingml.document",
                headers={"Content-Disposition": f"attachment; filename={request.title or 'rfp_qa'}.docx"}
            )
        else:  # txt
            text_content = export_service.export_to_text(content)
            
            return Response(
                content=text_content,
                media_type="text/plain",
                headers={"Content-Disposition": f"attachment; filename={request.title or 'rfp_qa'}.txt"}
            )
        
    except HTTPException as e:
        raise e
    except Exception as e:
        logger.error(f"Error exporting Q&A pairs: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Export failed: {str(e)}")

@router.get("/formats")
def get_export_formats():
    """Get supported export formats and features"""
    return export_service.get_supported_formats()
