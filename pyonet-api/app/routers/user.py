from fastapi import APIRouter
from app.libraries.libuser import User
from app.schemas.auth import UserModel, UserCreateModel, UserUpdateModel, UserJoinedModel
from app.tools.p3tools import get_schema

router = APIRouter(tags=["user"])
oUser = User()

@router.get("/user/schema")
async def get_user_schema(joined: bool = False):  
    create_schema = await get_schema(UserCreateModel)
    update_schema = await get_schema(UserUpdateModel)
    return { "create": create_schema, "update": update_schema }

@router.get("/user")
async def get_user_list(joined: bool = False, limit: int = 100, offset: int = 0, sortField: str = None, sortOrder: str = "asc", search: str = ""):
    return await oUser.get_user_list(joined=joined, limit=limit, offset=offset, sortField=sortField, sortOrder=sortOrder, search=search)

@router.get("/user/{userid}")
async def get_user(userid: int, joined: bool = False):
    return await oUser.get_user(userid, joined=joined)

@router.post("/user")
async def create_user(user: UserCreateModel):
    return await oUser.create_user(user)

@router.put("/user/{userid}")
async def update_user(userid: int, user: UserUpdateModel):
    return await oUser.update_user(userid, user)

@router.delete("/user/{userid}")
async def delete_user(userid: int):
    return await oUser.delete_user(userid)

