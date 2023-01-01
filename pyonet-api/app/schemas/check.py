from pydantic import BaseModel
from fastapi import Query
from typing import Optional    


class CheckModel(BaseModel):          
    checkid: Optional[int]  = Query(None, title="checkid", form_options={"optional":1,"display":0}) 
    name: str  = Query(..., title="name", max_length=32, form_options={}) 
    description: Optional[str]  = Query(None, title="description", max_length=128, form_options={})
    check_type: str  = Query(..., title="check_type", max_length=16, form_options={}) 
    check_interval: int
    config_json: str  = Query(..., title="config_json", max_length=64, form_options={})

class CheckCreateModel(BaseModel):
    name: str  = Query(..., title="name", max_length=32, form_options={}) 
    description: Optional[str]  = Query(None, title="description", max_length=128, form_options={})
    check_type: str  = Query(..., title="check_type", max_length=16, form_options={}) 
    check_interval: int
    config_json: str  = Query(..., title="config_json", max_length=64, form_options={})

class CheckUpdateModel(BaseModel):
    name: Optional[str]  = Query(..., title="name", max_length=32, form_options={}) 
    check_type: Optional[str]  = Query(..., title="check_type", max_length=16, form_options={}) 
    config_json: Optional[str]  = Query(..., title="config_json", form_options={})


class CheckJoinedModel(CheckModel):
    pass