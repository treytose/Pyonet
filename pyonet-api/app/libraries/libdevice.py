from http.client import HTTPException
from app import db
from app.schemas.device import DeviceModel, DeviceJoinedModel

class Device:
    async def __join_device__(self, device):

        return DeviceJoinedModel ( **device)


    async def generate(self):
        await db.create_schema("device", DeviceModel.schema())

    async def get_device_schema(self, joined: bool = False):
        schema = DeviceJoinedModel.schema() if joined else DeviceModel.schema()
        for v in schema['properties'].values():
            allowed_values = v.get("form_options", {}).get("allowed_values")
            if allowed_values and isinstance(allowed_values, str) and str.startswith(allowed_values.upper(), "SELECT"):                                
                v["form_options"]["allowed_values"] = await db.fetchall(allowed_values)                            
        return schema

    async def get_device_list(self, joined: bool = False, limit: int = 100, offset: int = 0, sortField: str = None, sortOrder: str = 'asc', search: str = ''): 
        sortSql = ""
        searchSql = ""
        injectObject = {}

        schema = await self.get_device_schema()

        if sortField:                        
            sortOrder = 'desc' if sortOrder.lower() == 'asc' else 'asc'
            if not sortField in schema['properties'].keys():
                raise HTTPException(status_code=400, detail='Invalid sortField')                
            sortSql = f"ORDER BY {sortField} {sortOrder}"

        if search:
            searchSql = 'WHERE '
            searchItems = []
            for name in schema['properties'].keys():
                searchItems.append(f'{name} LIKE :search_{name}')
                injectObject[f"search_{name}"] = f'%{search}%'

            searchSql += " OR ".join(searchItems)                                
                    
        device_list = await db.fetchall(f"SELECT * FROM `device` {searchSql} {sortSql} LIMIT {offset}, {limit}", injectObject)

        total_count = await db.fetchone("SELECT count(*) as count FROM `device`")
        count = await db.fetchone(f"SELECT count(*) as count FROM `device` {searchSql}", injectObject)
        meta = {
            "total_count": total_count["count"],
            "count": count["count"]
        }

        if not joined:
            return {"meta": meta, "data": device_list}

        device_list = [await self.__join_device__(item) for item in device_list]
        return {"meta": meta, "data": device_list}

    async def get_device(self, deviceid: int, joined: bool = False):
        device = await db.fetchone("SELECT * FROM `device` WHERE deviceid=:deviceid", {"deviceid": deviceid})
        if joined:
            device = self.__join_device__(device)
        return device

    async def create_device(self, device: DeviceModel):
        deviceid = await db.insert("device", device.dict())
        return deviceid

    async def update_device(self, deviceid: int, device: DeviceModel):
        error_no = await db.update("device", "deviceid", deviceid, device.dict())
        return error_no

    async def delete_device(self, deviceid: int):
        error_no = await db.delete("device", "deviceid", deviceid)
        return error_no