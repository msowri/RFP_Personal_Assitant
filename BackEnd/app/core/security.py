from datetime import datetime, timedelta, timezone
import jwt
from app.core.config import settings

def create_access_token(data: dict) -> str:    
    minutes = settings.ACCESS_TOKEN_EXPIRE_MINUTES or 30   
    expire = datetime.now(timezone.utc) + timedelta(minutes=minutes)
    to_encode = data.copy()
    to_encode.update({"exp": expire})    
    return jwt.encode(to_encode, settings.SECRET_KEY or "secret-temp-key", algorithm="HS256")

def decode_token(token: str) -> dict:   
    return jwt.decode(token, settings.SECRET_KEY or "secret-temp-key", algorithms=["HS256"])

#for testing purpose only
def verify_security_config(token: str) -> bool:
    try:
        #decode_token(token)        
        print(f"Loading Config from: {settings.model_config.get('env_file', 'Not Found')}")    
        print(f"App Name: {settings.APP_NAME or 'Not Found'}")  
        return True
    except jwt.ExpiredSignatureError:
        return False
    except jwt.InvalidTokenError:
        return False