import os
import uuid
import logging
from pathlib import Path
from datetime import datetime
from app.core.config import settings
import PyPDF2
from docx import Document

logger = logging.getLogger(__name__)


class FileService:
    def __init__(self):
        """Initialize FileService with upload directory"""
        self.upload_dir = Path(settings.UPLOAD_DIR)
        self.upload_dir.mkdir(exist_ok=True)
        logger.info(f"Upload directory initialized: {self.upload_dir}")
    
    def validate_file(self, filename: str, file_size: int) -> tuple[bool, str]:
        """
        Validate file size and type
        
        Args:
            filename: Name of the file
            file_size: Size of the file in bytes
        
        Returns:
            Tuple of (is_valid, message)
        """
        
        max_size_bytes = settings.MAX_FILE_SIZE_MB * 1024 * 1024
        if file_size > max_size_bytes:
            return False, f"File exceeds {settings.MAX_FILE_SIZE_MB}MB limit"
        
        
        file_extension = filename.split('.')[-1].lower()
        if file_extension not in settings.ALLOWED_FILE_TYPES:
            return False, f"File type '.{file_extension}' not allowed. Allowed: {', '.join(settings.ALLOWED_FILE_TYPES)}"
        
        return True, "Valid"
    
    def save_file(self, file_content: bytes, filename: str) -> dict:
        """
        Save file and return metadata
        
        Args:
            file_content: Binary content of the file
            filename: Original filename
        
        Returns:
            Dict with file metadata
        """
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
        """
        Extract text from uploaded file
        
        Args:
            file_path: Path to the file
        
        Returns:
            Extracted text content
        """
        file_extension = file_path.split('.')[-1].lower()
        
        if file_extension == "pdf":
            return self._extract_pdf(file_path)
        elif file_extension == "txt":
            return self._extract_txt(file_path)
        elif file_extension == "docx":
            return self._extract_docx(file_path)
        else:
            raise ValueError(f"Unsupported file type: {file_extension}")
    
    def _extract_pdf(self, file_path: str) -> str:
        """Extract text from PDF"""
        text = ""
        try:
            with open(file_path, 'rb') as f:
                reader = PyPDF2.PdfReader(f)
                for page in reader.pages:
                    page_text = page.extract_text()
                    if page_text:
                        text += page_text
            logger.info(f"Extracted {len(text)} characters from PDF")
        except Exception as e:
            logger.error(f"Error extracting PDF: {str(e)}")
            raise
        return text
    
    def _extract_txt(self, file_path: str) -> str:
        """Extract text from TXT"""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                text = f.read()
            logger.info(f"Extracted {len(text)} characters from TXT")
            return text
        except Exception as e:
            logger.error(f"Error extracting TXT: {str(e)}")
            raise
    
    def _extract_docx(self, file_path: str) -> str:
        """Extract text from DOCX"""
        text = ""
        try:
            doc = Document(file_path)
            for para in doc.paragraphs:
                text += para.text + "\n"
            logger.info(f"Extracted {len(text)} characters from DOCX")
        except Exception as e:
            logger.error(f"Error extracting DOCX: {str(e)}")
            raise
        return text
    
    def delete_file(self, file_path: str) -> bool:
        """
        Delete a file
        
        Args:
            file_path: Path to the file
        
        Returns:
            True if deleted, False otherwise
        """
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
        """Get file information"""
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