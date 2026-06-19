from pydantic import BaseModel


class UploadResponse(BaseModel):
    video_id: str
    filename: str


class TranscriptSegment(BaseModel):
    start: float
    end: float
    text: str


class TranscriptResponse(BaseModel):
    video_id: str
    language: str
    segments: list[TranscriptSegment]
