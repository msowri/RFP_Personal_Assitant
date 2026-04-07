from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.core.config import settings

if not settings.DATABASE_URL or not settings.DATABASE_URL.startswith("postgresql"):
    raise ValueError(
        "Invalid DATABASE_URL "
        "verify in environment file"
    )

engine = create_engine(
    settings.DATABASE_URL,
    pool_size=10,           
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