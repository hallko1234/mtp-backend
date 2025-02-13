# files.py - Datei-Uploads & Optimierung

from fastapi import APIRouter, File, UploadFile, BackgroundTasks, HTTPException
import shutil
import os
import subprocess
from PIL import Image
from PyPDF2 import PdfReader, PdfWriter
from config import UPLOAD_DIR, MAX_VIDEO_SIZE_MB

router_files = APIRouter(prefix="/files", tags=["files"])

def compress_image(file_path: str):
    """Komprimiert Bilder unter 1MB mit optimierter JPEG-Qualität."""
    try:
        img = Image.open(file_path).convert("RGB")
        quality = 85
        while quality > 50:
            img.save(file_path, "JPEG", quality=quality, optimize=True)
            if os.path.getsize(file_path) < 1000000:
                break
            quality -= 5
    except Exception as e:
        print(f"Fehler bei Bildverarbeitung: {e}")

def compress_video(file_path: str):
    """Komprimiert Videos mit FFmpeg (H.264, 720p, optimierte Bitrate)."""
    try:
        compressed_path = file_path.rsplit(".", 1)[0] + "_compressed.mp4"
        command = ["ffmpeg", "-i", file_path, "-vcodec", "libx264", "-crf", "28", "-preset", "slow", compressed_path]
        subprocess.run(command, check=True)
        os.replace(compressed_path, file_path)
    except subprocess.CalledProcessError as e:
        print(f"Fehler bei Video-Verarbeitung: {e}")

def optimize_pdf(file_path: str):
    """Reduziert die Größe von PDFs durch Entfernen unnötiger Metadaten."""
    try:
        reader = PdfReader(file_path)
        writer = PdfWriter()
        for page in reader.pages:
            writer.add_page(page)
        with open(file_path, "wb") as f:
            writer.write(f)
    except Exception as e:
        print(f"Fehler bei PDF-Optimierung: {e}")

@router_files.post("/upload")
def upload_file(file: UploadFile = File(...), background_tasks: BackgroundTasks):
    """Hochladen von Dateien mit Hintergrundoptimierung für Bilder, Videos & PDFs."""
    file_path = f"{UPLOAD_DIR}{file.filename}"
    file_size = file.file.seek(0, os.SEEK_END)
    file.file.seek(0)

    if file.filename.lower().endswith(("mp4", "avi", "mov", "mkv")) and file_size > MAX_VIDEO_SIZE_MB * 1024 * 1024:
        raise HTTPException(status_code=413, detail=f"Video zu groß! Maximal erlaubt: {MAX_VIDEO_SIZE_MB} MB")

    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    if file.filename.lower().endswith(("jpg", "jpeg", "png")):
        background_tasks.add_task(compress_image, file_path)
    elif file.filename.lower().endswith(("mp4", "avi", "mov", "mkv")):
        background_tasks.add_task(compress_video, file_path)
    elif file.filename.lower().endswith("pdf"):
        background_tasks.add_task(optimize_pdf, file_path)

    return {"message": "Upload erfolgreich"}

@router_files.get("/download/{filename}")
def download_file(filename: str):
    """Ermöglicht den Download einer gespeicherten Datei."""
    file_path = os.path.join(UPLOAD_DIR, filename)
    if not os.path.exists(file_path):
        raise HTTPException(status_code=404, detail="Datei nicht gefunden")
    return {"download_url": f"/static/{filename}"}
