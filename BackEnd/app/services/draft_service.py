from sqlalchemy.orm     import Session
from app.domain.entity.draft import Draft   
from app.domain.schemadto.draftdto import DraftCreate, DraftUpdate, DraftResponse
from app.repositories.draft_repository import create_draft, get_draft, update_draft, delete_draft 

class DraftService:
    def create_draft(self, db: Session, draft_data: DraftCreate) -> DraftResponse:
        draft = Draft(**draft_data.dict())
        created_draft = create_draft(db, draft)
        return DraftResponse.from_orm(created_draft)

    def get_draft(self, db: Session, draft_id: int) -> DraftResponse:
        draft = get_draft(db, draft_id)
        if not draft:
            raise ValueError("Draft not found")
        return DraftResponse.from_orm(draft)

    def update_draft(self, db: Session, draft_id: int, draft_data: DraftUpdate) -> DraftResponse:
        updated_fields = {k: v for k, v in draft_data.dict().items() if v is not None}
        updated_draft = update_draft(db, draft_id, updated_fields)
        if not updated_draft:
            raise ValueError("Draft not found")
        return DraftResponse.from_orm(updated_draft)

    def delete_draft(self, db: Session, draft_id: int) -> bool:
        return delete_draft(db, draft_id)
    
    def list_drafts(self, db: Session, limit: int = 100, offset: int = 0) -> list:
        from app.repositories.draft_repository import list_drafts
        drafts = list_drafts(db, limit=limit, offset=offset)
        return [
            {
                'id': draft.id,
                'question': draft.question,
                'answer': draft.answer,
                'document_id': draft.document_id,
                'is_edited': draft.is_edited,
                'created_on': str(draft.created_on),
                'updated_on': str(draft.updated_on)
            }
            for draft in drafts
        ]

    def get_drafts_by_document(self, db: Session, document_id: int) -> list:
        """Get all drafts for a specific document"""
        from app.repositories.draft_repository import get_drafts_by_document
        drafts = get_drafts_by_document(db, document_id)
        return [
            {
                'id': draft.id,
                'question': draft.question,
                'answer': draft.answer,
                'is_edited': draft.is_edited,
                'created_on': str(draft.created_on),
                'updated_on': str(draft.updated_on)
            }
            for draft in drafts
        ]