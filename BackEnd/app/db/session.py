from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.core.config import settings
import os
from dotenv import load_dotenv
load_dotenv()
DATABASE_URL = os.getenv("DATABASE_URL")

print(f"Using DATABASE_URL: {DATABASE_URL}")

if not DATABASE_URL or not DATABASE_URL.startswith("postgresql"):
    raise ValueError(
        "Invalid DATABASE_URL "
        "verify in environment file"
    )

engine = create_engine(
    DATABASE_URL,
    pool_size=25,    # for testing ony added       
    max_overflow=20,        
    pool_timeout=30,        
    pool_recycle=1800, 
)

SessionLocal = sessionmaker(
    autocommit=False, 
    autoflush=False, 
    bind=engine
)

def get_db(): #DI
    """
    Yields a database session to the FastAPI route and ensures     
    """
    db = SessionLocal()
    try:
        yield db          
    finally:
        db.close()