from pydantic import BaseModel
from fastapi import Query
from typing import Optional
from datetime import datetime
from typing import List
from app.schemas.role import RoleModel

class UserModel(BaseModel):    
    username: str = Query(..., max_length=64)
    create_date: Optional[datetime] = Query(None, description='Date and time the user signed up', form_options={"display": False})

class UserInDB(UserModel):    
    userid: int = Query(None)
    hashed_password: str = Query(..., max_length=128)

class UserJoinedModel(UserInDB):
    roles: List[RoleModel] = Query([], description='List of roles assigned to the user')

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    username: Optional[str] = None

class LoginModel(BaseModel):
    username: str = Query(None, max_length=64)
    password: str = Query(None, min_length=8)

class UserCreateModel(UserModel):
    password: str = Query(None, min_length=8)
    roles: Optional[List[int]] = Query([], description='List of roles to assign to the user')

class UserUpdateModel(UserModel):
    password: Optional[str] = Query(None, min_length=8)
    roles: Optional[List[int]] = Query([], description='List of roles to assign to the user')