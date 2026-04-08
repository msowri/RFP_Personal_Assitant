from fastapi import FastAPI

from app.core.config import settings
from app.core.security import verify_security_config

app= FastAPI()

@app.get("/")
def home():
    return {"message": "Test  Message"}

#test only
@app.get("/test_security_config")
def test_security_config():
    token = "test-token"
    if verify_security_config(token):
        print("Security configuration is valid.")
    else:
        print("Security configuration is invalid.")

