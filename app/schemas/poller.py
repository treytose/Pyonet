from pydantic import BaseModel
from fastapi import Query
from typing import Optional    


class PollerModel(BaseModel):          
    pollerid: Optional[int]  = Query(None, title="pollerid", form_options={"optional":1,"display":0}) 
    name: str  = Query(..., title="name", max_length=64, form_options={}) 
    description: str  = Query(..., title="description", max_length=256, form_options={}) 
    api_key: str  = Query(..., title="api_key", max_length=128, form_options={})
    hostname: str  = Query(..., title="hostname", max_length=128, form_options={})
    port: int  = Query(..., title="port", form_options={})

class PollerCreateModel(BaseModel):
    name: str  = Query(..., title="name", max_length=64, form_options={}) 
    description: str  = Query(..., title="description", max_length=256, form_options={}) 
    api_key: str  = Query(..., title="api_key", max_length=128, form_options={})

class PollerUpdateModel(BaseModel):
    name: Optional[str]  = Query(..., title="name", max_length=64, form_options={}) 
    description: Optional[str]  = Query(..., title="description", max_length=256, form_options={}) 
    api_key: Optional[str]  = Query(..., title="api_key", max_length=128, form_options={})


class PollerJoinedModel(PollerModel):
    pass