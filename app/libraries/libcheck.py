from http.client import HTTPException
from app import db
from app.schemas.check import DeviceCheckModel, DeviceCheckJoinedModel, DeviceCheckGroupModel

class Check:
    async def __join_check__(self, check):
        return DeviceCheckJoinedModel ( **check)

    async def generate(self):
        pass

    async def get_check_schema(self, joined: bool = False):
        schema = DeviceCheckJoinedModel.schema() if joined else DeviceCheckModel.schema()
        for v in schema['properties'].values():
            allowed_values = v.get("form_options", {}).get("allowed_values")
            if allowed_values and isinstance(allowed_values, str) and str.startswith(allowed_values.upper(), "SELECT"):                                
                v["form_options"]["allowed_values"] = await db.fetchall(allowed_values)                            
        return schema

    async def get_check_list(self, joined: bool = False, limit: int = 100, offset: int = 0, sortField: str = None, sortOrder: str = 'asc', search: str = ''): 
        sortSql = ""
        searchSql = ""
        injectObject = {}

        schema = await self.get_check_schema()

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
                    
        check_list = await db.fetchall(f"SELECT * FROM device_check {searchSql} {sortSql} LIMIT {offset}, {limit}", injectObject)

        total_count = await db.fetchone("SELECT count(*) as count FROM device_check")
        count = await db.fetchone(f"SELECT count(*) as count FROM device_check {searchSql}", injectObject)
        meta = {
            "total_count": total_count["count"],
            "count": count["count"]
        }

        if not joined:
            return {"meta": meta, "data": check_list}

        check_list = [await self.__join_check__(item) for item in check_list]
        return {"meta": meta, "data": check_list}

    async def get_check_list_by_device(self, deviceid: int, joined: bool = False, grouped: bool = False):
        check_list = await db.fetchall("SELECT * FROM device_check WHERE deviceid=:deviceid", {"deviceid": deviceid})
        if not joined and not grouped:
            return check_list
        
        if joined:
            check_list = [await self.__join_check__(item) for item in check_list]
        
        grouped_checks = {}
        checks_without_group = []
        if grouped:
            device_check_groups = await db.fetchall("SELECT * FROM device_check_group WHERE deviceid=:deviceid", {"deviceid": deviceid})
            
            for check_group in device_check_groups:
                grouped_checks[check_group["device_check_groupid"]] = dict(check_group)
                grouped_checks[check_group["device_check_groupid"]]["checks"] = []                
                
            for check in check_list:
                if check["device_check_groupid"]:
                    grouped_checks[check["device_check_groupid"]]["checks"].append(check)
                else:
                    checks_without_group.append(check)
                    
            return {"groups": grouped_checks, "checks": checks_without_group}
                                                
        return check_list

    async def get_check(self, device_checkid: int, joined: bool = False):
        check = await db.fetchone("SELECT * FROM device_check WHERE device_checkid=:device_checkid", {"device_checkid": device_checkid})
        if joined:
            check = self.__join_check__(check)
        return check

    async def create_check(self, check: DeviceCheckModel):
        device_checkid = await db.insert("device_check", check.dict())
        return device_checkid

    async def update_check(self, device_checkid: int, check: DeviceCheckModel):
        error_no = await db.update("device_check", "device_checkid", device_checkid, check.dict())
        return error_no

    async def delete_check(self, device_checkid: int):
        error_no = await db.delete("device_check", "device_checkid", device_checkid)
        return error_no
    
    
    ################## device-check-group ##################
    async def create_device_check_group(self, check_group: DeviceCheckGroupModel):
        device_check_groupid = await db.insert("device_check_group", check_group.dict())
        return device_check_groupid