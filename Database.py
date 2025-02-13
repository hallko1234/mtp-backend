# database.py - SQLite/PostgreSQL-Datenbank

from sqlalchemy import create_engine, Column, Integer, String, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import os

# Datenbankverbindung aus Umgebungsvariablen oder SQLite als Fallback
DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./mtp.db")
engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False} if "sqlite" in DATABASE_URL else {})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

def create_db():
    """Erstellt die Datenbanktabellen, falls sie nicht existieren."""
    Base.metadata.create_all(bind=engine)
