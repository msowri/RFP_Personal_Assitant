from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from app.services.question_extraction_service import QuestionExtractionService
from app.services.document_service import DocumentService
from app.db.session import get_db
from pydantic import BaseModel
from typing import List, Optional
import logging

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/api/questions", tags=["Question Extraction"])
question_service = QuestionExtractionService()
doc_service = DocumentService()

class QuestionExtractionRequest(BaseModel):
    document_id: Optional[int] = None
    text: Optional[str] = None
    store: Optional[bool] = False

class QuestionResponse(BaseModel):
    questions: List[str]
    total_questions: int
    source: str
    stored_questions: Optional[int] = None

@router.post("/extract", response_model=QuestionResponse)
async def extract_questions(
    request: QuestionExtractionRequest,
    db: Session = Depends(get_db)
):
    """Extract questions from document or raw text"""
    try:
        if request.document_id:
            document = doc_service.get_document(db, request.document_id)
            if not document:
                raise HTTPException(status_code=404, detail="Document not found")
            chunks = doc_service.get_chunks_by_document(db, request.document_id, limit=50)
            text = " ".join([chunk.chunk_text for chunk in chunks])
            source = f"Document ID: {request.document_id}"
        elif request.text:
            text = request.text
            source = "Provided text"
        else:
            raise HTTPException(status_code=400, detail="Either document_id or text must be provided")

        if not text or len(text.strip()) < 100:
            raise HTTPException(status_code=400, detail="Insufficient text for question extraction")

        questions = await question_service.extract_questions_from_text(text)
        if not questions:
            questions = question_service.extract_questions_by_patterns(text)
            source += " (pattern-based fallback)"

        stored_count = None
        if request.store:
            stored_questions = question_service.store_questions(db, request.document_id, questions)
            stored_count = len(stored_questions)

        return QuestionResponse(
            questions=questions,
            total_questions=len(questions),
            source=source,
            stored_questions=stored_count
        )

    except HTTPException as e:
        raise e
    except Exception as e:
        logger.error(f"Error extracting questions: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Question extraction failed: {str(e)}")

@router.get("/document/{document_id}")
def get_document_questions(document_id: int, db: Session = Depends(get_db)):
    questions = question_service.get_questions_for_document(db, document_id)
    return {
        "document_id": document_id,
        "questions": [
            {
                "id": q.id,
                "question_text": q.question_text,
                "normalized_text": q.normalized_text,
                "is_extracted": q.is_extracted,
                "created_on": str(q.created_on)
            }
            for q in questions
        ]
    }

@router.get("/patterns")
def get_extraction_patterns():
    """Get information about question extraction patterns"""
    return {
        "ai_based": {
            "description": "Uses AI to understand context and extract meaningful questions",
            "features": ["Context understanding", "Question quality filtering", "Duplicate removal"]
        },
        "pattern_based": {
            "description": "Uses regex patterns to find question structures",
            "patterns": [
                "What...?", "How...?", "When...?", "Where...?", "Why...?", 
                "Which...?", "Who...?", "Please provide...?", "Can you...?"
            ]
        },
        "fallback": "Pattern-based extraction is used as fallback when AI extraction fails"
    }
