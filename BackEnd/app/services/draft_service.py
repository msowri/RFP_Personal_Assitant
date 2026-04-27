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