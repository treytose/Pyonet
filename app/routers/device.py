import requests
from fastapi import APIRouter, Depends
from pydantic import BaseModel
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


########################### Device Poller forwarding ###########################
class DevicePollerQuery(BaseModel):
    deviceid: int
    route: str
    params: dict = {}
    payload: dict = {}
    method: str = "GET"
    
@router.post("/device-poller")
async def query_device_poller(query: DevicePollerQuery):
    device = await oDevice.get_device(query.deviceid, joined=True)
    poller = device.poller
    
    if not device:
        return {"error": "Device not found"}
    
    if not poller:
        return {"error": "Device has no poller"}
    
    route = query.route
    if route.startswith("/"):
        route = route[1:]
            
    url = f"http://{poller.hostname}:{poller.port}/{route}"
    headers = {
        "PYONET-POLLER-API-KEY": f"{poller.api_key}"
    }
    
    if query.method == "GET":
        response = requests.get(url, headers=headers, params=query.params)
    elif query.method == "POST":
        response = requests.post(url, headers=headers, params=query.params, json=query.payload)
    else:
        return {"error": "Unknown method"}
    
    return response.json()
    
    
    
    