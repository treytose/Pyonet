from fastapi import APIRouter, Depends
from app.libraries.libdevice import Device
from app.schemas.device import DeviceModel, DeviceUpdateModel, DeviceCreateModel
from app.dependencies import verify_token

router = APIRouter(tags=["device"], dependencies=[Depends(verify_token)])
oDevice = Device()

@router.get("/device/schema")
async def get_device_schema(joined: bool = False):              
  return await oDevice.get_device_schema(joined=joined)        

@router.get("/device")
async def get_device_list(joined: bool = False, limit: int = 100, offset: int = 0, sortField: str = None, sortOrder: str = "asc", search: str = ""):
    return await oDevice.get_device_list(joined=joined, limit=limit, offset=offset, sortField=sortField, sortOrder=sortOrder, search=search)

@router.get("/device/{deviceid}")
async def get_device(deviceid: int, joined: bool = False):
    return await oDevice.get_device(deviceid, joined=joined)

@router.post("/device")
async def create_device(device: DeviceCreateModel):
    return await oDevice.create_device(device)

@router.put("/device/{deviceid}")
async def update_device(deviceid: int, device: DeviceUpdateModel):
    return await oDevice.update_device(deviceid, device)

@router.delete("/device/{deviceid}")
async def delete_device(deviceid: int):
    return await oDevice.delete_device(deviceid)
    
    