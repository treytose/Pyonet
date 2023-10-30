from pydantic import BaseModel
from fastapi import Query
from typing import Optional    


class DeviceCheckModel(BaseModel):          
    device_checkid: Optional[int]  = Query(None, title="checkid", form_options={"optional":1,"display":0}) 
    deviceid: int  = Query(..., title="deviceid", form_options={})
    device_check_groupid: Optional[int]  = Query(None, title="device_check_groupid", form_options={"optional":1,"display":0})
    name: str  = Query(..., title="name", max_length=32, form_options={}) 
    description: Optional[str]  = Query(None, title="description", max_length=128, form_options={})
    check_type: str  = Query(..., title="check_type", max_length=16, form_options={}) 
    check_interval: int
    oid: Optional[str]  = Query(None, title="oid", max_length=64, form_options={})

class CheckCreateModel(BaseModel):
    deviceid: int  = Query(..., title="deviceid", form_options={})
    name: str  = Query(..., title="name", max_length=32, form_options={}) 
    description: Optional[str]  = Query(None, title="description", max_length=128, form_options={})
    check_type: str  = Query(..., title="check_type", max_length=16, form_options={}) 
    check_interval: int
    oid: Optional[str]  = Query(None, title="oid", max_length=64, form_options={})

class CheckUpdateModel(BaseModel):    
    name: Optional[str]  = Query(..., title="name", max_length=32, form_options={}) 
    description: Optional[str]  = Query(None, title="description", max_length=128, form_options={})
    check_type: Optional[str]  = Query(..., title="check_type", max_length=16, form_options={}) 
    check_interval: Optional[int]
    oid: Optional[str]  = Query(None, title="oid", max_length=64, form_options={})


class DeviceCheckJoinedModel(DeviceCheckModel):
    pass

class DeviceCheckGroupModel(BaseModel):
    device_check_groupid: Optional[int]  = Query(None, title="device_check_groupid", form_options={"optional":1,"display":0})
    deviceid: int  = Query(..., title="deviceid", form_options={})
    name: str  = Query(..., title="name", max_length=32, form_options={})
    description: Optional[str]  = Query(None, title="description", max_length=128, form_options={})