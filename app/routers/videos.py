import shutil
import uuid
from pathlib import Path

from fastapi import APIRouter, HTTPException, UploadFile
from fastapi.responses import FileResponse

from app.config import UPLOADS_DIR
from app.models.schemas import UploadResponse

router = APIRouter(prefix="/videos", tags=["videos"])

VIDEO_EXTENSIONS = {".mp4", ".mov", ".webm", ".mkv", ".avi"}
AUDIO_EXTENSIONS = {".mp3", ".wav", ".m4a", ".aac", ".ogg", ".flac"}
ALLOWED_EXTENSIONS = VIDEO_EXTENSIONS | AUDIO_EXTENSIONS


@router.post("/upload", response_model=UploadResponse)
async def upload_video(file: UploadFile) -> UploadResponse:
    suffix = Path(file.filename or "").suffix.lower()
    if suffix not in ALLOWED_EXTENSIONS:
        raise HTTPException(status_code=400, detail=f"Formato no soportado: {suffix}")

    video_id = uuid.uuid4().hex
    dest_path = UPLOADS_DIR / f"{video_id}{suffix}"

    with dest_path.open("wb") as out_file:
        shutil.copyfileobj(file.file, out_file)

    return UploadResponse(
        video_id=video_id,
        filename=dest_path.name,
        is_audio=suffix in AUDIO_EXTENSIONS,
    )


@router.get("/{video_id}/file")
async def get_video_file(video_id: str) -> FileResponse:
    matches = list(UPLOADS_DIR.glob(f"{video_id}.*"))
    if not matches:
        raise HTTPException(status_code=404, detail="Video no encontrado")
    return FileResponse(matches[0])


def resolve_video_path(video_id: str) -> Path:
    matches = list(UPLOADS_DIR.glob(f"{video_id}.*"))
    if not matches:
        raise HTTPException(status_code=404, detail="Video no encontrado")
    return matches[0]
