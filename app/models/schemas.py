from pydantic import BaseModel


class UploadResponse(BaseModel):
    video_id: str
    filename: str
    is_audio: bool


class TranscriptSegment(BaseModel):
    start: float
    end: float
    text: str


class TranscriptResponse(BaseModel):
    video_id: str
    language: str
    segments: list[TranscriptSegment]


class TranscriptSegmentUpdate(BaseModel):
    text: str | None = None
    start: float | None = None
    end: float | None = None
