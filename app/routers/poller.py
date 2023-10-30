from fastapi import APIRouter, Depends
from app.dependencies import verify_api_key
from app.libraries.libpoller import Poller
from app.schemas.poller import PollerModel, PollerUpdateModel, PollerCreateModel

router = APIRouter(tags=["poller"])
oPoller = Poller()


# Poller Requests ( API_KEY required )

@router.get("/poller/devices")
async def get_poller_devices(poller = Depends(verify_api_key)):
    return await oPoller.get_poller_devices(poller)

# CRUID Poller Requests ( JWT required )

@router.get("/poller/schema")
async def get_poller_schema(joined: bool = False):              
  return await oPoller.get_poller_schema(joined=joined)        

@router.get("/poller")
async def get_poller_list(joined: bool = False, limit: int = 100, offset: int = 0, sortField: str = None, sortOrder: str = "asc", search: str = ""):
    return await oPoller.get_poller_list(joined=joined, limit=limit, offset=offset, sortField=sortField, sortOrder=sortOrder, search=search)

@router.get("/poller/{pollerid}")
async def get_poller(pollerid: int, joined: bool = False):
    return await oPoller.get_poller(pollerid, joined=joined)

@router.post("/poller")
async def create_poller(poller: PollerCreateModel):
    return await oPoller.create_poller(poller)

@router.put("/poller/{pollerid}")
async def update_poller(pollerid: int, poller: PollerUpdateModel):
    return await oPoller.update_poller(pollerid, poller)

@router.delete("/poller/{pollerid}")
async def delete_poller(pollerid: int):
    return await oPoller.delete_poller(pollerid)

