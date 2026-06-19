import shutil
import uuid
from pathlib import Path

from fastapi import APIRouter, HTTPException, UploadFile
from fastapi.responses import FileResponse

from app.config import UPLOADS_DIR
from app.models.schemas import UploadResponse
from app.services.export import export_with_burned_subtitles
from app.services.transcript_store import load_transcript

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


@router.post("/{video_id}/export")
async def export_video(video_id: str) -> FileResponse:
    source_path = resolve_video_path(video_id)

    transcript = load_transcript(video_id)
    if transcript is None or not transcript["segments"]:
        raise HTTPException(status_code=400, detail="El video no tiene transcripcion para quemar")

    is_audio = source_path.suffix.lower() in AUDIO_EXTENSIONS

    try:
        output_path = export_with_burned_subtitles(
            video_id, source_path, transcript["segments"], is_audio=is_audio
        )
    except RuntimeError as exc:
        raise HTTPException(status_code=500, detail=str(exc)) from exc

    return FileResponse(output_path, filename=output_path.name, media_type="video/mp4")
