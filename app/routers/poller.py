import requests
from urllib3.exceptions import NewConnectionError
from pydantic import BaseModel
from fastapi import APIRouter, Depends, HTTPException
from app.dependencies import verify_api_key, verify_token
from app.libraries.libpoller import Poller
from app.schemas.poller import PollerModel, PollerUpdateModel, PollerCreateModel

router = APIRouter(tags=["poller"])
oPoller = Poller()


# Poller Requests ( API_KEY required )

@router.get("/poller/devices")
async def get_poller_devices(poller = Depends(verify_api_key)):
    return await oPoller.get_poller_devices(poller)

class PollerQuery(BaseModel):
    pollerid: int
    route: str
    params: dict = {}
    payload: dict = {}
    method: str = "GET"

@router.post("/query-poller")
async def query_poller(query: PollerQuery, user = Depends(verify_token)):
    poller = await oPoller.get_poller(query.pollerid)
    
    if not poller:
        raise HTTPException(status_code=404, detail="Poller not found")
    
    try:
        route = query.route
        if route.startswith("/"):
            route = route[1:]
            
        url = f"http://{poller.hostname}:{poller.port}/{route}"
        headers = {
            "PYONET-POLLER-API-KEY": f"{poller.api_key}"
        }
        
        if query.method == "GET":
            r = requests.get(url, headers=headers, params=query.params)
        elif query.method == "POST":
            r = requests.post(url, headers=headers, params=query.params, json=query.payload)
        elif query.method == "PUT":
            r = requests.put(url, headers=headers, params=query.params, json=query.payload)
        elif query.method == "DELETE":
            r = requests.delete(url, headers=headers, params=query.params)
        else:
            return {"error": "Invalid method"}
        
        return r.json()        
    except requests.exceptions.ConnectionError as e:
        raise HTTPException(status_code=500, detail="Unable to connect to poller")
    except Exception as e2:
        print(e2)
        raise HTTPException(status_code=500, detail="Poller error")        
    
# CRUD Poller Requests ( JWT required )

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

