# models.py - Datenbank-Modelle

from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from database import Base

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)
    password = Column(String)
    role = Column(String, default="standard")

class File(Base):
    __tablename__ = "files"
    id = Column(Integer, primary_key=True, index=True)
    filename = Column(String)
    folder = Column(String)
    owner_id = Column(Integer, ForeignKey("users.id"))
    owner = relationship("User")

class ShareLink(Base):
    __tablename__ = "share_links"
    id = Column(Integer, primary_key=True, index=True)
    filename = Column(String)
    expiration = Column(Integer)
