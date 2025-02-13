# share.py - QR-Code Link-Freigabe

from fastapi import APIRouter, HTTPException
import time
from database import SessionLocal
from models import ShareLink

router_share = APIRouter(prefix="/share", tags=["share"])

def get_db():
    """Erstellt eine neue Datenbank-Session."""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router_share.post("/create/{filename}")
def create_temp_link(filename: str, db: SessionLocal = next(get_db())):
    """Erstellt einen temporären Freigabe-Link für eine Datei (gültig für 2 Stunden)."""
    expiry = int(time.time()) + 7200  # 2 Stunden
    temp_link = ShareLink(filename=filename, expiration=expiry)
    db.add(temp_link)
    db.commit()
    return {"download_link": f"/share/download/{filename}"}

@router_share.get("/download/{filename}")
def download_temp_file(filename: str, db: SessionLocal = next(get_db())):
    """Ermöglicht den Download einer Datei über einen temporären Link."""
    temp_link = db.query(ShareLink).filter(ShareLink.filename == filename).first()
    if not temp_link or temp_link.expiration < int(time.time()):
        raise HTTPException(status_code=403, detail="Link abgelaufen oder ungültig")
    return {"download_url": f"/static/{filename}"}
