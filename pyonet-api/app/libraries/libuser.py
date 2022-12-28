from fastapi import HTTPException
from datetime import datetime
from app import db
from app.libraries.libauth import Auth
from app.schemas.auth import UserModel, UserJoinedModel, UserCreateModel, UserUpdateModel


class User:
    def __init__(self):
        self.oAuth = Auth()

    async def __join_user__(self, user):
        roles = await db.fetchall('''
            SELECT r.* FROM user_role_link url
                INNER JOIN role r ON r.roleid = url.roleid
            WHERE url.userid = :userid
        ''', {"userid": user.userid})        
        return UserJoinedModel ( **user, roles=roles)

    async def generate(self):
        await db.create_schema("user", UserModel.schema())

    async def get_user_schema(self, joined: bool = False):
        schema = UserJoinedModel.schema() if joined else UserModel.schema()
        for v in schema['properties'].values():
            allowed_values = v.get("form_options", {}).get("allowed_values")
            if allowed_values and isinstance(allowed_values, str) and str.startswith(allowed_values.upper(), "SELECT"):                                
                v["form_options"]["allowed_values"] = await db.fetchall(allowed_values)                            
        
        return schema

    async def get_user_list(self, joined: bool = False, limit: int = 100, offset: int = 0, sortField: str = None, sortOrder: str = 'asc', search: str = ''): 
        sortSql = ""
        searchSql = ""
        injectObject = {}

        schema = await self.get_user_schema()

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
                    
        user_list = await db.fetchall(f"SELECT * FROM `user` {searchSql} {sortSql} LIMIT {offset}, {limit}", injectObject)

        total_count = await db.fetchone("SELECT count(*) as count FROM `user`")
        count = await db.fetchone(f"SELECT count(*) as count FROM `user` {searchSql}", injectObject)
        meta = {
            "total_count": total_count["count"],
            "count": count["count"]
        }

        if not joined:
            return {"meta": meta, "data": user_list}

        user_list = [await self.__join_user__(item) for item in user_list]
        return {"meta": meta, "data": user_list}

    async def get_user(self, userid: int, joined: bool = False):
        user = await db.fetchone("SELECT * FROM `user` WHERE userid=:userid", {"userid": userid})
        if joined:
            user = self.__join_user__(user)
        return user

    async def create_user(self, user: UserCreateModel):
        user.create_date = datetime.now()      
        userid = await self.oAuth.create_user(user)
        if not userid:
            raise HTTPException(status_code=400, detail="An error occurred while creating the user.")
    
        for roleid in user.roles:
            await db.insert("user_role_link", {"userid": userid, "roleid": roleid})

        return userid

    async def update_user(self, userid: int, user: UserUpdateModel):
        user_model = UserModel(**user.dict())
        error_no = await db.update("user", "userid", userid, user_model.dict(exclude_none=True))

        if error_no == 0:
            await db.delete("user_role_link", "userid", userid)
            for roleid in user.roles:
                await db.insert("user_role_link", {"userid": userid, "roleid": roleid})

        return error_no

    async def delete_user(self, userid: int):
        error_no = await db.delete("user", "userid", userid)
        return error_no
    
