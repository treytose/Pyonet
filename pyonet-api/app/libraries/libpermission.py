from http.client import HTTPException
from app import db
from app.schemas.permission import PermissionModel, PermissionJoinedModel

class Permission:
    async def __join_permission__(self, permission):

        return PermissionJoinedModel ( **permission)


    async def generate(self):
        await db.create_schema("permission", PermissionModel.schema())

    async def get_permission_schema(self, joined: bool = False):
        schema = PermissionJoinedModel.schema() if joined else PermissionModel.schema()
        for v in schema['properties'].values():
            allowed_values = v.get("form_options", {}).get("allowed_values")
            if allowed_values and isinstance(allowed_values, str) and str.startswith(allowed_values.upper(), "SELECT"):                                
                v["form_options"]["allowed_values"] = await db.fetchall(allowed_values)                            
        return schema

    async def get_permission_list(self, joined: bool = False, limit: int = 100, offset: int = 0, sortField: str = None, sortOrder: str = 'asc', search: str = ''): 
        sortSql = ""
        searchSql = ""
        injectObject = {}

        schema = await self.get_permission_schema()

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
                    
        permission_list = await db.fetchall(f"SELECT * FROM `permission` {searchSql} {sortSql} LIMIT {offset}, {limit}", injectObject)

        total_count = await db.fetchone("SELECT count(*) as count FROM `permission`")
        count = await db.fetchone(f"SELECT count(*) as count FROM `permission` {searchSql}", injectObject)
        meta = {
            "total_count": total_count["count"],
            "count": count["count"]
        }

        if not joined:
            return {"meta": meta, "data": permission_list}

        permission_list = [await self.__join_permission__(item) for item in permission_list]
        return {"meta": meta, "data": permission_list}

    async def get_permission(self, permissionid: int, joined: bool = False):
        permission = await db.fetchone("SELECT * FROM `permission` WHERE permissionid=:permissionid", {"permissionid": permissionid})
        if joined:
            permission = self.__join_permission__(permission)
        return permission

    async def create_permission(self, permission: PermissionModel):
        permissionid = await db.insert("permission", permission.dict())
        return permissionid

    async def update_permission(self, permissionid: int, permission: PermissionModel):
        error_no = await db.update("permission", "permissionid", permissionid, permission.dict())
        return error_no

    async def delete_permission(self, permissionid: int):
        error_no = await db.delete("permission", "permissionid", permissionid)
        return error_no