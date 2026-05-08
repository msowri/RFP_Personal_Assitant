from sqlalchemy.orm import Session
from app.domain.entity.question import Question


def create_question(db: Session, question: Question):
    db.add(question)
    db.commit()
    db.refresh(question)
    return question


def bulk_create_questions(db: Session, questions: list[Question]):
    db.add_all(questions)
    db.commit()
    for question in questions:
        db.refresh(question)
    return questions


def get_questions_by_document(db: Session, document_id: int):
    return db.query(Question).filter(Question.document_id == document_id).all()
