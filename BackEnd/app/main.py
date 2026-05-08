from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import logging

from app.core.config import settings
from app.core.security import verify_security_config
from app.db.base import Base
from app.db.session import engine
import app.domain.entity.documents
import app.domain.entity.draft
import app.domain.entity.question
from app.routers import file_router, document_router
from app.routers import query_router
from app.routers import draft_router
from app.routers import question_router
from app.routers import export_router


Base.metadata.create_all(bind=engine)



# Configure logging
logging.basicConfig(level=logging.INFO) # for future use only added
logger = logging.getLogger(__name__)

app = FastAPI(
    title="RFP Personal Assistant API",
    version="1.0.0",
    description="API for RFP document processing and analysis"
)

# Enable CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://localhost:5173", "*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Register routers
app.include_router(file_router.router)
app.include_router(document_router.router)
app.include_router(query_router.router)
app.include_router(draft_router.router)
app.include_router(question_router.router)
app.include_router(export_router.router)

@app.get("/")
def home():
    return {
        "message": "RFP Personal Assistant API",
        "version": "1.0.0",
        "docs": "/docs",
        "redoc": "/redoc"
    }

@app.get("/health")
def health_check():
    return {"status": "healthy", "app": settings.APP_NAME}

@app.get("/test_security_config")
def test_security_config():
    token = "test-token"
    if verify_security_config(token):
        print("Security configuration is valid.")
    else:
        print("Security configuration is invalid.")

