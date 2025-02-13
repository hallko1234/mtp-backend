# sync.py - API für die Synchronisation

from fastapi import APIRouter, HTTPException
import os
from config import UPLOAD_DIR

router_sync = APIRouter(prefix="/sync", tags=["sync"])

@router_sync.get("/check")
def check_updates():
    """Überprüft die zuletzt geänderten Dateien im Upload-Verzeichnis."""
    try:
        files = os.listdir(UPLOAD_DIR)
        file_info = [{"filename": f, "last_modified": os.path.getmtime(os.path.join(UPLOAD_DIR, f))} for f in files]
        return sorted(file_info, key=lambda x: x["last_modified"], reverse=True)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Fehler beim Abrufen der Dateien: {str(e)}")
