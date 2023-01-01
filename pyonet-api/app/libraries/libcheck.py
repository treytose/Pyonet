from http.client import HTTPException
from app import db
from app.schemas.check import CheckModel, CheckJoinedModel

class Check:
    async def __join_check__(self, check):

        return CheckJoinedModel ( **check)


    async def generate(self):
        await db.create_schema("check", CheckModel.schema())

    async def get_check_schema(self, joined: bool = False):
        schema = CheckJoinedModel.schema() if joined else CheckModel.schema()
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
                    
        check_list = await db.fetchall(f"SELECT * FROM `check` {searchSql} {sortSql} LIMIT {offset}, {limit}", injectObject)

        total_count = await db.fetchone("SELECT count(*) as count FROM `check`")
        count = await db.fetchone(f"SELECT count(*) as count FROM `check` {searchSql}", injectObject)
        meta = {
            "total_count": total_count["count"],
            "count": count["count"]
        }

        if not joined:
            return {"meta": meta, "data": check_list}

        check_list = [await self.__join_check__(item) for item in check_list]
        return {"meta": meta, "data": check_list}

    async def get_check(self, checkid: int, joined: bool = False):
        check = await db.fetchone("SELECT * FROM `check` WHERE checkid=:checkid", {"checkid": checkid})
        if joined:
            check = self.__join_check__(check)
        return check

    async def create_check(self, check: CheckModel):
        checkid = await db.insert("check", check.dict())
        return checkid

    async def update_check(self, checkid: int, check: CheckModel):
        error_no = await db.update("check", "checkid", checkid, check.dict())
        return error_no

    async def delete_check(self, checkid: int):
        error_no = await db.delete("check", "checkid", checkid)
        return error_no