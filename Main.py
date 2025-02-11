import os
import logging
from fastapi import FastAPI
from auth import router_auth
from routes.files import router_files
from routes.users import router_users
from routes.sync import router_sync
from routes.share import router_share
from database import create_db

# Logging einrichten
LOG_DIR = "logs/"
if not os.path.exists(LOG_DIR):
    os.makedirs(LOG_DIR)
LOG_FILE = f"{LOG_DIR}server.log"
logging.basicConfig(filename=LOG_FILE, level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

# Server starten
app = FastAPI(title="MTP Server API", version="1.0")
app.include_router(router_auth)
app.include_router(router_files)
app.include_router(router_users)
app.include_router(router_sync)
app.include_router(router_share)

@app.get("/")
def home():
    return {"message": "MTP Server läuft!"}

# Datenbank initialisieren
create_db()
