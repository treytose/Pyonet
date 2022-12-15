from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer, APIKeyHeader
from app.libraries.libauth import Auth
from jwt.exceptions import ExpiredSignatureError, InvalidSignatureError
from app import db

oAuth = Auth()

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/login/form")

async def verify_token(token: str = Depends(oauth2_scheme)):      
    if not token or token == "null":
        raise HTTPException(status_code=401, detail="Not authenticated")          

    try:
        user = await oAuth.get_current_user(token)
    except ExpiredSignatureError as e:
        raise HTTPException(status_code=401, detail="Token expired")    
    except InvalidSignatureError as ie:
        raise HTTPException(status_code=401, detail="Bad token")    
        
    if not user:
        raise HTTPException(status_code=401, detail="Bad token")

    return user

async def verify_api_key(api_key: str = Depends(APIKeyHeader(name="Authorization", auto_error=False, description="Pyonet-Poller API key"))):    
    if not api_key or api_key == "null":
        raise HTTPException(status_code=401, detail="Not authenticated")          

    # check for API key in database
    poller = await db.fetchone("SELECT * FROM poller WHERE api_key = :api_key", {"api_key": api_key})
    if not poller:
        raise HTTPException(status_code=401, detail="Bad API key")

    return poller
