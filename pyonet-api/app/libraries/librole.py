from http.client import HTTPException
from app import db
from app.schemas.role import RoleModel, RoleJoinedModel, RoleUpdateModel, RoleCreateModel

class Role:
    async def __join_role__(self, role):
        if role.name == "admin":
            permissions = await db.fetchall('SELECT * FROM permission')
        else:
            permissions = await db.fetchall('''
                SELECT p.* FROM permission p
                    INNER JOIN role_permission_link rpl ON rpl.permissionid = p.permissionid
                WHERE rpl.roleid = :roleid
            ''', {"roleid": role.roleid})
        return RoleJoinedModel ( **role, permissions=permissions)


    async def generate(self):
        await db.create_schema("role", RoleModel.schema())

    async def get_role_schema(self, joined: bool = False):
        schema = RoleJoinedModel.schema() if joined else RoleModel.schema()
        for v in schema['properties'].values():
            allowed_values = v.get("form_options", {}).get("allowed_values")
            if allowed_values and isinstance(allowed_values, str) and str.startswith(allowed_values.upper(), "SELECT"):                                
                v["form_options"]["allowed_values"] = await db.fetchall(allowed_values)                            
        return schema

    async def get_role_list(self, joined: bool = False, limit: int = 100, offset: int = 0, sortField: str = None, sortOrder: str = 'asc', search: str = ''): 
        sortSql = ""
        searchSql = ""
        injectObject = {}

        schema = await self.get_role_schema()

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
                    
        role_list = await db.fetchall(f"SELECT * FROM `role` {searchSql} {sortSql} LIMIT {offset}, {limit}", injectObject)

        total_count = await db.fetchone("SELECT count(*) as count FROM `role`")
        count = await db.fetchone(f"SELECT count(*) as count FROM `role` {searchSql}", injectObject)
        meta = {
            "total_count": total_count["count"],
            "count": count["count"]
        }

        if not joined:
            return {"meta": meta, "data": role_list}

        role_list = [await self.__join_role__(item) for item in role_list]
        return {"meta": meta, "data": role_list}

    async def get_role(self, roleid: int, joined: bool = False):
        role = await db.fetchone("SELECT * FROM `role` WHERE roleid=:roleid", {"roleid": roleid})
        if joined:
            role = self.__join_role__(role)
        return role

    async def create_role(self, role_create: RoleCreateModel):
        role = RoleModel(**role_create.dict())
        roleid = await db.insert("role", role.dict())

        for permissionid in role_create.permissions:
            await db.insert("role_permission_link", {"roleid": roleid, "permissionid": permissionid})
            
        return roleid

    async def update_role(self, roleid: int, role_update: RoleUpdateModel):
        role = RoleModel(**role_update.dict())
        error_no = await db.update("role", "roleid", roleid, role.dict(exclude_unset=True))

        await db.delete("role_permission_link", "roleid", roleid)

        for permissionid in role_update.permissions:
            await db.insert("role_permission_link", {"roleid": roleid, "permissionid": permissionid})

        return error_no

    async def delete_role(self, roleid: int):
        error_no = await db.delete("role", "roleid", roleid)
        return error_no