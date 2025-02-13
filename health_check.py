# health_check.py - Backend- und Server-Überprüfung

from fastapi import APIRouter
import os
import shutil
import socket
import platform
import importlib.util
from config import UPLOAD_DIR, MAX_VIDEO_SIZE_MB, SECRET_KEY
from database import DATABASE_URL

router_health = APIRouter(prefix="/health", tags=["health"])

# Liste der erforderlichen Module
REQUIRED_MODULES = [
    "fastapi",
    "os",
    "shutil",
    "socket",
    "platform",
    "sqlalchemy",
    "bcrypt",
    "jwt",
    "PIL",
    "PyPDF2",
    "subprocess"
]

def check_modules():
    """Überprüft, ob alle erforderlichen Module installiert sind."""
    missing_modules = []
    for module in REQUIRED_MODULES:
        if importlib.util.find_spec(module) is None:
            missing_modules.append(module)
    return missing_modules

@router_health.get("/check")
def system_check():
    """Überprüft die Servereinstellungen und gibt Statusinformationen zurück."""
    try:
        # Systeminformationen abrufen
        system_info = {
            "hostname": socket.gethostname(),
            "os": platform.system(),
            "os_version": platform.version(),
            "python_version": platform.python_version(),
        }
        
        # Speicherplatz überprüfen
        total, used, free = shutil.disk_usage("/")
        storage_info = {
            "total_space_gb": round(total / (1024 ** 3), 2),
            "used_space_gb": round(used / (1024 ** 3), 2),
            "free_space_gb": round(free / (1024 ** 3), 2),
        }
        
        # Überprüfung der Konfiguration
        config_info = {
            "upload_directory": UPLOAD_DIR,
            "max_video_size_mb": MAX_VIDEO_SIZE_MB,
            "database_url": DATABASE_URL,
            "secret_key_set": bool(SECRET_KEY),  # Prüft, ob ein SECRET_KEY gesetzt ist
        }
        
        # Überprüfung der erforderlichen Module
        missing_modules = check_modules()
        module_status = "OK" if not missing_modules else "Fehlende Module: " + ", ".join(missing_modules)
        
        return {
            "system_info": system_info,
            "storage_info": storage_info,
            "config_info": config_info,
            "module_check": module_status,
            "status": "OK" if not missing_modules else "ERROR",
        }
    except Exception as e:
        return {"status": "ERROR", "message": str(e)}
