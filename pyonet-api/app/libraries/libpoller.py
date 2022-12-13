from http.client import HTTPException
from app import db
from app.schemas.poller import PollerModel, PollerJoinedModel

class Poller:
    async def __join_poller__(self, poller):
        return PollerJoinedModel ( **poller)

    async def generate(self):
        await db.create_schema("poller", PollerModel.schema())

    async def get_poller_schema(self, joined: bool = False):
        schema = PollerJoinedModel.schema() if joined else PollerModel.schema()
        for v in schema['properties'].values():
            allowed_values = v.get("form_options", {}).get("allowed_values")
            if allowed_values and isinstance(allowed_values, str) and str.startswith(allowed_values.upper(), "SELECT"):                                
                v["form_options"]["allowed_values"] = await db.fetchall(allowed_values)                            
        return schema

    async def get_poller_list(self, joined: bool = False, limit: int = 100, offset: int = 0, sortField: str = None, sortOrder: str = 'asc', search: str = ''): 
        sortSql = ""
        searchSql = ""
        injectObject = {}

        schema = await self.get_poller_schema()

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
                    
        poller_list = await db.fetchall(f"SELECT * FROM `poller` {searchSql} {sortSql} LIMIT {offset}, {limit}", injectObject)

        total_count = await db.fetchone("SELECT count(*) as count FROM `poller`")
        count = await db.fetchone(f"SELECT count(*) as count FROM `poller` {searchSql}", injectObject)
        meta = {
            "total_count": total_count["count"],
            "count": count["count"]
        }

        if not joined:
            return {"meta": meta, "data": poller_list}

        poller_list = [await self.__join_poller__(item) for item in poller_list]
        return {"meta": meta, "data": poller_list}

    async def get_poller(self, pollerid: int, joined: bool = False):
        poller = await db.fetchone("SELECT * FROM `poller` WHERE pollerid=:pollerid", {"pollerid": pollerid})
        if joined:
            poller = self.__join_poller__(poller)
        return poller

    async def create_poller(self, poller: PollerModel):
        pollerid = await db.insert("poller", poller.dict())
        return pollerid

    async def update_poller(self, pollerid: int, poller: PollerModel):
        error_no = await db.update("poller", "pollerid", pollerid, poller.dict())
        return error_no

    async def delete_poller(self, pollerid: int):
        error_no = await db.delete("poller", "pollerid", pollerid)
        return error_no

    async def get_poller_devices(self, poller):
        devices = await db.fetchall("SELECT * FROM device WHERE pollerid = :pollerid", {"pollerid": poller.pollerid})
        return devices