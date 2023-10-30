from fastapi import APIRouter
from app.libraries.librole import Role
from app.schemas.role import RoleModel, RoleUpdateModel, RoleCreateModel

router = APIRouter(tags=["role"])
oRole = Role()

@router.get("/role/schema")
async def get_role_schema(joined: bool = False):              
  return await oRole.get_role_schema(joined=joined)        

@router.get("/role")
async def get_role_list(joined: bool = False, limit: int = 100, offset: int = 0, sortField: str = None, sortOrder: str = "asc", search: str = ""):
    return await oRole.get_role_list(joined=joined, limit=limit, offset=offset, sortField=sortField, sortOrder=sortOrder, search=search)

@router.get("/role/{roleid}")
async def get_role(roleid: int, joined: bool = False):
    return await oRole.get_role(roleid, joined=joined)

@router.post("/role")
async def create_role(role: RoleCreateModel):
    return await oRole.create_role(role)

@router.put("/role/{roleid}")
async def update_role(roleid: int, role: RoleUpdateModel):
    return await oRole.update_role(roleid, role)

@router.delete("/role/{roleid}")
async def delete_role(roleid: int):
    return await oRole.delete_role(roleid)