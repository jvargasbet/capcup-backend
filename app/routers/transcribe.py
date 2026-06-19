from fastapi import APIRouter

from app.models.schemas import TranscriptResponse, TranscriptSegment
from app.routers.videos import resolve_video_path
from app.services.transcription import transcribe_audio

router = APIRouter(prefix="/videos", tags=["transcription"])


@router.post("/{video_id}/transcribe", response_model=TranscriptResponse)
async def transcribe_video(video_id: str) -> TranscriptResponse:
    video_path = resolve_video_path(video_id)
    language, segments = transcribe_audio(str(video_path))

    return TranscriptResponse(
        video_id=video_id,
        language=language,
        segments=[TranscriptSegment(**seg) for seg in segments],
    )
