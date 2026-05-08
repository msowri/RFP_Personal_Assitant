import logging
from typing import List
from app.services.docai_service import DocAIService
from app.repositories.question_repository import create_question, bulk_create_questions, get_questions_by_document
from app.domain.entity.question import Question

logger = logging.getLogger(__name__)

class QuestionExtractionService:
    def __init__(self):
        self.ai_service = DocAIService()

    async def extract_questions_from_text(self, text: str) -> List[str]:
        """Extract questions from document text using AI"""
        try:
            prompt = f"""
You are an expert at analyzing RFP (Request for Proposal) documents.
Extract all questions from the following text.
Return only the questions, one per line, without numbering.

Text:
{text}

Questions:
"""

            response = await self.ai_service.ask_with_context("", prompt)
            
            questions = self._clean_question_lines(response)
            logger.info(f"Extracted {len(questions)} unique questions")
            return questions
        except Exception as e:
            logger.error(f"Error extracting questions: {str(e)}")
            return []

    def store_questions(self, db, document_id: int | None, questions: List[str]):
        stored_questions = []
        if not questions:
            return stored_questions

        question_entities = []
        for question_text in questions:
            normalized = self.normalize_question(question_text)
            question_entities.append(
                Question(
                    document_id=document_id,
                    question_text=question_text,
                    normalized_text=normalized,
                    is_extracted=True
                )
            )

        bulk_create_questions(db, question_entities)
        for question in question_entities:
            stored_questions.append({
                "id": question.id,
                "question_text": question.question_text,
                "normalized_text": question.normalized_text,
                "document_id": question.document_id
            })
        return stored_questions

    def get_questions_for_document(self, db, document_id: int):
        return get_questions_by_document(db, document_id)

    def normalize_question(self, question: str) -> str:
        result = question.strip()
        result = result.replace('1.', '').replace('2.', '').replace('3.', '')
        result = result.replace('1)', '').replace('2)', '').replace('3)', '')
        return result

    def extract_questions_by_patterns(self, text: str) -> List[str]:
        """Extract questions using regex patterns as fallback"""
        import re
        
        question_patterns = [
            r'[^.!?]*\?[^.!?]*',
            r'What\s+[^.!?]*\?',
            r'How\s+[^.!?]*\?',
            r'When\s+[^.!?]*\?',
            r'Where\s+[^.!?]*\?',
            r'Why\s+[^.!?]*\?',
            r'Which\s+[^.!?]*\?',
            r'Who\s+[^.!?]*\?',
            r'Please\s+provide[^.!?]*\?',
            r'Can\s+you[^.!?]*\?',
        ]
        
        questions = []
        for pattern in question_patterns:
            matches = re.findall(pattern, text, re.IGNORECASE)
            for match in matches:
                question = match.strip()
                if len(question) > 10 and question.endswith('?'):
                    questions.append(question)
        
        return list(dict.fromkeys(questions))[:20]

    def _clean_question_lines(self, response: str) -> List[str]:
        questions = []
        for line in response.split('\n'):
            line = line.strip()
            if line and '?' in line:
                question = self.normalize_question(line)
                if question and question.endswith('?'):
                    questions.append(question)
        return list(dict.fromkeys(questions))
