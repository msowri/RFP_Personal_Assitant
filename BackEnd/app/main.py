from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import logging

from app.core.config import settings
from app.core.security import verify_security_config
from app.routers import file_router, document_router
#from app.routers importquery_router


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

# Register 
app.include_router(file_router.router)
app.include_router(document_router.router)

@app.get("/")
def home():
    return {
        "message": "RFP Personal Assistant API",
        "version": "1.0.0",
        "docs": "/docs",
        "redoc": "/redoc"
    }

# @app.get("/health")
# def health_check():
#     return {"status": "healthy", "app": settings.APP_NAME}

@app.get("/test_security_config")
def test_security_config():
    token = "test-token"
    if verify_security_config(token):
        print("Security configuration is valid.")
    else:
        print("Security configuration is invalid.")

