# users.py - Benutzerverwaltung API

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database import SessionLocal
from models import User
import bcrypt

router_users = APIRouter(prefix="/users", tags=["users"])

def get_db():
    """Erzeugt eine neue Datenbank-Session für jede Anfrage."""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router_users.get("/")
def get_users(db: Session = Depends(get_db)):
    """Gibt eine Liste aller Benutzer zurück."""
    return db.query(User).all()

@router_users.post("/create")
def create_user(username: str, password: str, role: str = "standard", db: Session = Depends(get_db)):
    """Erstellt einen neuen Benutzer mit gehashtem Passwort."""
    hashed_pw = bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()
    new_user = User(username=username, password=hashed_pw, role=role)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return {"message": "Benutzer erstellt", "user": new_user.username}

@router_users.delete("/delete/{user_id}")
def delete_user(user_id: int, db: Session = Depends(get_db)):
    """Löscht einen Benutzer anhand der Benutzer-ID."""
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="Benutzer nicht gefunden")
    db.delete(user)
    db.commit()
    return {"message": "Benutzer gelöscht"}
