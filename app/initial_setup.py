import os, random
from rich import print
from rich.prompt import Prompt
from app.tools.asyncdb import AsyncDB

async def run_initial_setup():
  # ask if user wants to run initial setup
  print("[bold red]WARNING: .env file not found![/bold red]")
  
  run_setup = Prompt.ask("Would you like to run initial setup?", choices=["y", "n"], default="y")
  
  if run_setup == "n":
    print("[bold red]WARNING: .env file not found![/bold red]")
    print("[bold red]Exiting...[/bold red]")
    return
  
  # create .env file
  env_file = open(".env", "w")
  
  # generate SECRET_KEY
  print("[bold blue]Generating SECRET_KEY...[/bold blue]")
  SECRET_KEY = os.urandom(32).hex()
  env_file.write(f"SECRET_KEY={SECRET_KEY}\n")
  
  # generate ALGORITHM
  print("[bold blue]Generating ALGORITHM...[/bold blue]")
  ALGORITHM = "HS256"
  env_file.write(f"ALGORITHM={ALGORITHM}\n")
  
  # generate ACCESS_TOKEN_EXPIRE_MINUTES
  print("[bold blue]Generating ACCESS_TOKEN_EXPIRE_MINUTES...[/bold blue]")
  ACCESS_TOKEN_EXPIRE_MINUTES = 60 * 24 * 7 # 7 days
  env_file.write(f"ACCESS_TOKEN_EXPIRE_MINUTES={ACCESS_TOKEN_EXPIRE_MINUTES}\n")
  
  # ask for database connection info
  confirmed = False
  while not confirmed:
    print("[bold blue]Enter database connection info:[/bold blue]")
    db_host = Prompt.ask("Host", default="localhost")
    db_port = Prompt.ask("Port", default="5432")
    db_user = Prompt.ask("User")
    db_pass = Prompt.ask("Password")
    
    # test database connection
    print("[bold blue]Testing database connection...[/bold blue]")
    try:
      db = AsyncDB(db_host=db_host, db_port=db_port, db_user=db_user, db_pass=db_pass)
      await db.connect()
      await db.disconnect()
      print("[bold green]Successfully connected to database[/bold green]")
      break
    except Exception as e:
      print(f"[bold red]ERROR: {e}[/bold red]")
      continue
    
    
    
    
    
  
  
  
  
  
  
  
  
    
  