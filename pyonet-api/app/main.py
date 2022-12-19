from fastapi import Request, status, FastAPI
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from . import db

# routers 
from .routers import role
from .routers import user
from .routers import permission
from .routers import device
from .routers import poller
from .routers import auth

app = FastAPI()

@app.get("/hello")
async def hello():
    return "Hello World"

@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
	exc_str = f'{exc}'.replace('\n', ' ').replace('   ', ' ')
	print(f"{request}: {exc_str}")
	content = {'status_code': 10422, 'message': exc_str, 'data': None}
	return JSONResponse(content=content, status_code=status.HTTP_422_UNPROCESSABLE_ENTITY)


# app events #
@app.on_event("startup")
async def startup_event():
    await db.connect()
    await role.oRole.generate()
    await permission.oPermission.generate()
    await device.oDevice.generate()
    await poller.oPoller.generate()
    await auth.oAuth.generate()

@app.on_event("shutdown")
async def shutdown_event():
    await db.disconnect()


# register routers #
app.include_router(role.router)
app.include_router(user.router)
app.include_router(permission.router)
app.include_router(device.router)
app.include_router(poller.router)
app.include_router(auth.router)
