from fastapi import APIRouter
from app.libraries.libcheck import Check
from app.schemas.check import DeviceCheckModel, DeviceCheckGroupModel

router = APIRouter(tags=["check"])
oCheck = Check()

@router.get("/check/schema")
async def get_check_schema(joined: bool = False):              
  return await oCheck.get_check_schema(joined=joined)        

@router.get("/device-check")
async def get_check_list(joined: bool = False, limit: int = 100, offset: int = 0, sortField: str = None, sortOrder: str = "asc", search: str = ""):
    return await oCheck.get_check_list(joined=joined, limit=limit, offset=offset, sortField=sortField, sortOrder=sortOrder, search=search)

@router.get("/device-check/by-device/{deviceid}")
async def get_check_list_by_device(deviceid: int, joined: bool = False, grouped: bool = False):
    resp = await oCheck.get_check_list_by_device(deviceid, joined=joined, grouped=grouped)
    return resp

@router.get("/device-check/{device_checkid}")
async def get_check(device_checkid: int, joined: bool = False):
    return await oCheck.get_check(device_checkid, joined=joined)

@router.post("/device-check")
async def create_check(check: DeviceCheckModel):
    return await oCheck.create_check(check)

@router.put("/device-check/{device_checkid}")
async def update_check(device_checkid: int, check: DeviceCheckModel):
    return await oCheck.update_check(device_checkid, check)

@router.delete("/device-check/{device_checkid}")
async def delete_check(device_checkid: int):
    return await oCheck.delete_check(device_checkid)


############## device-check-group ################
@router.post("/device-check-group")
async def create_device_check_group(check_group: DeviceCheckGroupModel):
    return await oCheck.create_device_check_group(check_group)