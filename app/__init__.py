import os, asyncio
from dotenv import load_dotenv
from app.tools.asyncdb import AsyncDB


# check if .env exists
if not os.path.isfile(".env"):
    from .initial_setup import run_initial_setup
    
    loop = asyncio.get_event_loop()
    loop.run_until_complete(run_initial_setup())
    
    try: sys.exit(0)
    except: pass


# load environment variables from .env 
load_dotenv()

# db init #
db = AsyncDB()

# auth settings #
SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = os.getenv("ALGORITHM") or "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

if not SECRET_KEY:
    raise Exception("Missing required environment variable SECRET_KEY. Suggested: use 'openssl rand -hex 32' to create one and add it to the .env file.")
