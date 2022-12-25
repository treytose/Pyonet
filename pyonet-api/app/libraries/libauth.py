from datetime import datetime, timedelta
from fastapi import HTTPException
from app import db, SECRET_KEY, ALGORITHM
from app.schemas.auth import UserModel, UserInDB, TokenData, UserCreateModel, UserJoinedModel

from passlib.context import CryptContext
import jwt

class Auth:    
    def __init__(self):
      self.pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")  

    async def __join_user__(self, user: UserModel):        
        roles = await db.fetchall("SELECT role.* FROM user_role_link INNER JOIN role ON user_role_link.roleid = role.roleid WHERE user_role_link.userid = :userid", {"userid": user.userid})
        # give admin all permissions
        if "admin" in [role.name for role in roles]:
            permissions = await db.fetchall("SELECT * FROM permission")
        else:
            permissions = await db.fetchall('''
                SELECT permission.* FROM user_role_link url
                    INNER JOIN role_permission_link rpl ON url.roleid = rpl.roleid
                    INNER JOIN permission ON rpl.permissionid = permission.permissionid
                WHERE url.userid = :userid
            ''', {"userid": user.userid})
        return UserJoinedModel(**user.dict(), roles=[role.name for role in roles], permissions=[permission.name for permission in permissions])

    async def generate(self):
        await db.create_schema("user", UserInDB.schema()) 

    async def get_user(self, userid: int):
        user = await db.fetchone("SELECT * FROM user WHERE userid = :userid", {"userid": userid})                
        return UserInDB(**user)

    async def get_safe_user(self, userid: int):
        user = await self.get_user(userid)
        # return UserModel(**user.dict())
        return await self.__join_user__(user)

    async def get_user_by_username(self, username: str):
        user = await db.fetchone("SELECT * FROM user WHERE username = :username", {"username": username})
        if not user:
          return None
        return UserInDB(**user)
    
    async def verify_password(self, plain_password, hashed_password):
        return self.pwd_context.verify(plain_password, hashed_password)

    async def get_password_hash(self, password):
        return self.pwd_context.hash(password)

    async def create_user(self, user: UserCreateModel):
        if await self.get_user_by_username(user.username):
            raise HTTPException(status_code=400, detail="username already exists")

        hashed_password = await self.get_password_hash(user.password)
        user_dict = user.dict()
        del user_dict["password"]
        user_dict["hashed_password"] = hashed_password
        user_in_db = UserInDB(**user_dict)
        userid = await db.insert("user", user_in_db.dict())
        return userid

    async def authenticate_user(self, username: str, password: str):      
        user = await self.get_user_by_username(username)
        if not user:
            return False

        if not await self.verify_password(password, user.hashed_password):
            return False

        return await self.create_user_token(user)

    async def create_user_token(self, user: UserInDB, expires_delta: timedelta = None):
        token = await self.create_access_token(
            { "sub": user.userid }, 
            expires_delta
        )
        return token
    
    async def create_access_token(self, data: dict, expires_delta: timedelta = None):
        to_encode = data.copy()
        if expires_delta:
            expire = datetime.utcnow() + expires_delta
        else:
            expire = datetime.utcnow() + timedelta(days=7)
        to_encode.update({"exp": expire})
        encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
        return encoded_jwt

    async def get_current_user(self, token: str):           
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])        
        userid = payload.get("sub")                

        user = await self.get_safe_user(userid)
        return user

