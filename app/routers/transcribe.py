from fastapi import APIRouter, HTTPException

from app.models.schemas import TranscriptResponse, TranscriptSegment, TranscriptSegmentUpdate
from app.routers.videos import resolve_video_path
from app.services.transcript_store import load_transcript, save_transcript, update_segment
from app.services.transcription import transcribe_audio

router = APIRouter(prefix="/videos", tags=["transcription"])


@router.post("/{video_id}/transcribe", response_model=TranscriptResponse)
async def transcribe_video(video_id: str) -> TranscriptResponse:
    cached = load_transcript(video_id)
    if cached is not None:
        return TranscriptResponse(**cached)

    video_path = resolve_video_path(video_id)
    language, segments = transcribe_audio(str(video_path))
    save_transcript(video_id, language, segments)

    return TranscriptResponse(
        video_id=video_id,
        language=language,
        segments=[TranscriptSegment(**seg) for seg in segments],
    )


@router.patch("/{video_id}/transcript/{segment_index}", response_model=TranscriptResponse)
async def update_transcript_segment(
    video_id: str, segment_index: int, update: TranscriptSegmentUpdate
) -> TranscriptResponse:
    updated = update_segment(
        video_id,
        segment_index,
        text=update.text,
        start=update.start,
        end=update.end,
    )
    if updated is None:
        raise HTTPException(status_code=404, detail="Transcripcion o segmento no encontrado")

    return TranscriptResponse(**updated)
