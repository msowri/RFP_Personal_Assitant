import os
import uuid
from pathlib import Path
from datetime import datetime
from app.core.config import settings
import PyPDF2
from docx import Document

class FileService:
    def __init__(self):
        self.upload_dir = Path(settings.UPLOAD_DIR)
        self.upload_dir.mkdir(exist_ok=True)

        #implementation pending -progress