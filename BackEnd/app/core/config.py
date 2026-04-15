from pydantic_settings import BaseSettings
from typing import Optional 
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent.parent
ENV_PATH = BASE_DIR / ".env"

class Settings(BaseSettings):
    """ FPA settings."""   
    APP_NAME: str = "RFP Personal Assistant" 
    # DATABASE_URL: str = "postgresql://postgres:Gramener123@localhost:5432/rfppersonaldb"
    SECRET_KEY: Optional[str] = "temp-secret-key"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    UPLOAD_DIR: str = str(BASE_DIR / "uploads")
    MAX_FILE_SIZE_MB: int = 50
    ALLOWED_FILE_TYPES: list = ["pdf", "txt", "docx"]
    
    model_config = {
        "env_file": str(ENV_PATH),
        "env_file_encoding": "utf-8", 
        "extra": "ignore" 
    }

# Initialize settings object
settings = Settings()
