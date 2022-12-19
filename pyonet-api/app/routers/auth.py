from datetime import timedelta
from fastapi import APIRouter, Depends, Form, HTTPException
from pydantic import ValidationError
from app import ACCESS_TOKEN_EXPIRE_MINUTES
from app.dependencies import verify_token, verify_api_key
from app.schemas.auth import Token, LoginModel
from app.libraries.libauth import Auth

router = APIRouter()
oAuth = Auth()

@router.post("/auth/login/form", response_model=Token)
async def login_form(username: str = Form(...), password: str = Form(...)):
    token = await oAuth.authenticate_user(username, password)
    if not token:
        raise HTTPException(status_code=401, detail="Invalid username or password")
    return {"access_token": token, "token_type": "bearer"}

@router.post("/auth/login", response_model=Token)
async def login(login_model: LoginModel):
    token = await oAuth.authenticate_user(login_model.username, login_model.password)
    if not token:
        raise HTTPException(status_code=401, detail="Invalid username or password")
    return {"access_token": token, "token_type": "bearer"}


@router.get("/auth/verify")
async def verify(user = Depends(verify_token)):
    if not user:
        raise HTTPException(status_code=401, detail="Not authenticated")
    return user

@router.get("/auth/test")
async def test(user = Depends(verify_token)):
    return user

@router.get("/auth/test/api_key")
async def test_api_key(poller = Depends(verify_api_key)):
    return poller