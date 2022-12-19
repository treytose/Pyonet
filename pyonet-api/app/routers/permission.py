from fastapi import APIRouter
from app.libraries.libpermission import Permission
from app.schemas.permission import PermissionModel, PermissionUpdateModel, PermissionCreateModel

router = APIRouter(tags=["permission"])
oPermission = Permission()

@router.get("/permission/schema")
async def get_permission_schema(joined: bool = False):              
  return await oPermission.get_permission_schema(joined=joined)        

@router.get("/permission")
async def get_permission_list(joined: bool = False, limit: int = 100, offset: int = 0, sortField: str = None, sortOrder: str = "asc", search: str = ""):
    return await oPermission.get_permission_list(joined=joined, limit=limit, offset=offset, sortField=sortField, sortOrder=sortOrder, search=search)

@router.get("/permission/{permissionid}")
async def get_permission(permissionid: int, joined: bool = False):
    return await oPermission.get_permission(permissionid, joined=joined)

@router.post("/permission")
async def create_permission(permission: PermissionCreateModel):
    return await oPermission.create_permission(permission)

@router.put("/permission/{permissionid}")
async def update_permission(permissionid: int, permission: PermissionUpdateModel):
    return await oPermission.update_permission(permissionid, permission)

@router.delete("/permission/{permissionid}")
async def delete_permission(permissionid: int):
    return await oPermission.delete_permission(permissionid)