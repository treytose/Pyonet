from pydantic import BaseModel
from fastapi import Query
from typing import Optional    
from app.schemas.poller import PollerModel


class DeviceModel(BaseModel):          
    deviceid: Optional[int]  = Query(None, title="deviceid", form_options={"optional":1,"display":0}) 
    name: str  = Query(..., title="name", max_length=64, form_options={}) 
    description: str  = Query(..., title="description", max_length=128, form_options={}) 
    hostname: str  = Query(..., title="hostname", max_length=64, form_options={}) 
    snmp_version: str  = Query(..., title="snmp_version", max_length=8, form_options={}) 
    snmp_community: str  = Query(..., title="snmp_community", max_length=64, form_options={}) 
    snmp_port: int  = Query(161, title="snmp_port", form_options={})
    pollerid: int = Query(..., title="pollerid", form_options={}, foreign_key="poller.pollerid")

class DeviceCreateModel(BaseModel):
    name: str  = Query(..., title="name", max_length=64, form_options={}) 
    description: str  = Query(..., title="description", max_length=128, form_options={}) 
    hostname: str  = Query(..., title="hostname", max_length=64, form_options={}) 
    snmp_version: str  = Query(..., title="snmp_version", max_length=8, form_options={}) 
    snmp_community: str  = Query(..., title="snmp_community", max_length=64, form_options={}) 
    snmp_port: int  = Query(161, title="snmp_port", form_options={})
    pollerid: int = Query(..., title="pollerid", form_options={})

class DeviceUpdateModel(BaseModel):
    name: Optional[str]  = Query(..., title="name", max_length=64, form_options={}) 
    description: Optional[str]  = Query(..., title="description", max_length=128, form_options={}) 
    hostname: Optional[str]  = Query(..., title="hostname", max_length=64, form_options={}) 
    snmp_version: Optional[str]  = Query(..., title="snmp_version", max_length=8, form_options={}) 
    snmp_community: Optional[str]  = Query(..., title="snmp_community", max_length=64, form_options={}) 
    snmp_port: Optional[int]  = Query(161, title="snmp_port", form_options={})
    pollerid: int = Query(..., title="pollerid", form_options={})

class DeviceJoinedModel(DeviceModel):
    poller: PollerModel = Query(..., title="poller", form_options={}, joined=True)