from fastapi import APIRouter
from app.libraries.libcheck import Check
from app.schemas.check import CheckModel, CheckUpdateModel, CheckCreateModel

router = APIRouter(tags=["check"])
oCheck = Check()

@router.get("/check/schema")
async def get_check_schema(joined: bool = False):              
  return await oCheck.get_check_schema(joined=joined)        

@router.get("/check")
async def get_check_list(joined: bool = False, limit: int = 100, offset: int = 0, sortField: str = None, sortOrder: str = "asc", search: str = ""):
    return await oCheck.get_check_list(joined=joined, limit=limit, offset=offset, sortField=sortField, sortOrder=sortOrder, search=search)

@router.get("/check/{checkid}")
async def get_check(checkid: int, joined: bool = False):
    return await oCheck.get_check(checkid, joined=joined)

@router.post("/check")
async def create_check(check: CheckCreateModel):
    return await oCheck.create_check(check)

@router.put("/check/{checkid}")
async def update_check(checkid: int, check: CheckUpdateModel):
    return await oCheck.update_check(checkid, check)

@router.delete("/check/{checkid}")
async def delete_check(checkid: int):
    return await oCheck.delete_check(checkid)