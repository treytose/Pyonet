from pydantic import BaseModel
from fastapi import Query
from typing import Optional    


class PermissionModel(BaseModel):          
    permissionid: Optional[int]  = Query(None, title="permissionid", form_options={"optional":1,"display":0}) 
    name: str  = Query(..., title="name", max_length=32, form_options={}) 
    description: str  = Query(..., title="description", max_length=128, form_options={})

class PermissionCreateModel(BaseModel):
    name: str  = Query(..., title="name", max_length=32, form_options={}) 
    description: str  = Query(..., title="description", max_length=128, form_options={})

class PermissionUpdateModel(BaseModel):
    name: Optional[str]  = Query(..., title="name", max_length=32, form_options={}) 
    description: Optional[str]  = Query(..., title="description", max_length=128, form_options={})


class PermissionJoinedModel(PermissionModel):
      pass