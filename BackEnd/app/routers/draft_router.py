from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.services.draft_service import DraftService 
from app.domain.schemadto.draftdto import DraftCreate, DraftUpdate, DraftResponse
from app.db.session import get_db

router = APIRouter(prefix="/drafts", tags=["Drafts"])

service = DraftService()

@router.post("/", response_model=DraftResponse)
def create_draft(draft_data: DraftCreate, db: Session = Depends(get_db)):       
    return service.create_draft(db, draft_data) 


@router.get("/{draft_id}", response_model=DraftResponse)
def read_draft(draft_id: int, db: Session = Depends(get_db)):    
    return service.get_draft(db, draft_id)

@router.put("/{draft_id}", response_model=DraftResponse)
def update_draft(draft_id: int, draft_data: DraftUpdate, db: Session  = Depends(get_db)):
    return service.update_draft(db, draft_id, draft_data)   

@router.delete("/{draft_id}")   
def delete_draft(draft_id: int, db: Session = Depends(get_db)):
    success = service.delete_draft(db, draft_id)
    if not success:
        raise ValueError("Draft not found")
    return {"message": "Draft deleted successfully"}