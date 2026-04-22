import os
import uuid
import logging
from pathlib import Path
from datetime import datetime
from app.core.config import settings
#import PyPDF2
from docx import Document
import pdfplumber

logger = logging.getLogger(__name__)


class FileService:
    def __init__(self):
       
        self.upload_dir = Path(settings.UPLOAD_DIR)
        self.upload_dir.mkdir(exist_ok=True)
        logger.info(f"Upload directory initialized: {self.upload_dir}")
    
    def validate_file(self, filename: str, file_size: int) -> tuple[bool, str]:
       
        max_size_bytes = settings.MAX_FILE_SIZE_MB * 1024 * 1024
        if file_size > max_size_bytes:
            return False, f"File exceeds {settings.MAX_FILE_SIZE_MB}MB limit"
        
        
        file_extension = filename.split('.')[-1].lower()
        if file_extension not in settings.ALLOWED_FILE_TYPES:
            return False, f"File type '.{file_extension}' not allowed. Allowed: {', '.join(settings.ALLOWED_FILE_TYPES)}"
        
        return True, "Valid"
    
    def save_file(self, file_content: bytes, filename: str) -> dict:
       
        file_id = str(uuid.uuid4())
        file_extension = filename.split('.')[-1].lower()
        stored_filename = f"{file_id}.{file_extension}"
        file_path = self.upload_dir / stored_filename
        
        # Save file
        with open(file_path, 'wb') as f:
            f.write(file_content)
        
        logger.info(f"File saved: {stored_filename} (ID: {file_id})")
        
        return {
            "file_id": file_id,
            "original_name": filename,
            "stored_name": stored_filename,
            "file_path": str(file_path),
            "size_bytes": len(file_content),
            "uploaded_at": datetime.now().isoformat(),
            "file_type": file_extension
        }
    
    def extract_text(self, file_path: str) -> str:
        
        file_extension = file_path.split('.')[-1].lower()
        
        if file_extension == "pdf":
            return self._extract_pdf(file_path)
        elif file_extension == "txt":
            return self._extract_txt(file_path)
        elif file_extension == "docx":
            return self._extract_docx(file_path)
        else:
            raise ValueError(f"Unsupported file type: {file_extension}")
    
    # def _extract_pdf(self, file_path: str) -> str:
    #     """Extract text from PDF"""
    #     text = ""
    #     try:
    #         with open(file_path, 'rb') as f:
    #             reader = PyPDF2.PdfReader(f)
    #             for page in reader.pages:
    #                 page_text = page.extract_text()
    #                 if page_text:
    #                     text += page_text
    #         logger.info(f"Extracted {len(text)} characters from PDF")
    #     except Exception as e:
    #         logger.error(f"Error extracting PDF: {str(e)}")
    #         raise
    #     return text
    
    def _extract_pdf(self, file_path: str) -> str:
        text = ""
        with pdfplumber.open(file_path) as pdf:
            for page in pdf.pages:
                content = page.extract_text()
                if content:
                    text += content + "\n"
        return text
    
    def _extract_txt(self, file_path: str) -> str:
       
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                text = f.read()
            logger.info(f"Extracted {len(text)} characters from TXT")
            return text
        except Exception as e:
            logger.error(f"Error extracting TXT: {str(e)}")
            raise
    
    def _extract_docx(self, file_path: str) -> str:  

      doc = Document(file_path)
      return "\n".join([p.text.strip() for p in doc.paragraphs if p.text.strip()])
    
    def delete_file(self, file_path: str) -> bool:
        
        try:
            if os.path.exists(file_path):
                os.remove(file_path)
                logger.info(f"File deleted: {file_path}")
                return True
            return False
        except Exception as e:
            logger.error(f"Error deleting file: {str(e)}")
            return False
    
    def get_file_info(self, file_path: str) -> dict:
        
        try:
            if os.path.exists(file_path):
                stat = os.stat(file_path)
                return {
                    "path": file_path,
                    "size_bytes": stat.st_size,
                    "size_mb": round(stat.st_size / (1024 * 1024), 2),
                    "created_at": datetime.fromtimestamp(stat.st_ctime).isoformat(),
                    "modified_at": datetime.fromtimestamp(stat.st_mtime).isoformat()
                }
            return None # type: ignore
        except Exception as e:
            logger.error(f"Error getting file info: {str(e)}")
            return None # type: ignore
