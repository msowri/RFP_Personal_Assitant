from sqlalchemy.orm import Session
from app.domain.entity.draft import Draft   


def create_draft(db: Session, draft: Draft):
    db.add(draft)
    db.commit()
    db.refresh(draft)
    return draft    

def get_draft(db: Session, draft_id: int):
    return db.query(Draft).filter(Draft.id == draft_id).first()     

def update_draft(db: Session, draft_id: int, updated_fields: dict):
    draft = db.query(Draft).filter(Draft.id == draft_id).first()
    if not draft:
        return None
    for key, value in updated_fields.items():
        setattr(draft, key, value)
    db.commit()
    db.refresh(draft)
    return draft

def delete_draft(db: Session, draft_id: int):
    draft = db.query(Draft).filter(Draft.id == draft_id).first()
    if not draft:
        return False
    db.delete(draft)
    db.commit()
    return True

def get_drafts_by_document(db: Session, document_id: int):
    return db.query(Draft).filter(Draft.document_id == document_id).all()


def list_drafts(db: Session, limit: int = 100, offset: int = 0):
    return db.query(Draft).order_by(Draft.created_on.desc()).limit(limit).offset(offset).all()