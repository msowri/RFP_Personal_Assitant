from pydantic_settings import BaseSettings
from typing import Optional 
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent.parent
ENV_PATH = BASE_DIR / ".env"

class Settings(BaseSettings):
    """ FPA settings."""   
    APP_NAME: str = "RFP Personal Assistant" 
    DATABASE_URL: Optional[str] = "postgresql://postgres:Gramener123@localhost:5432/rfppersonaldb" # change in future 
    SECRET_KEY: Optional[str] = "temp-secret-key" #change in future
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    model_config = {
        "env_file": str(ENV_PATH),
        "env_file_encoding": "utf-8", 
        "extra": "ignore" 
    }
# init setting object
settings = Settings()
