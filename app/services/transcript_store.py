import json
from pathlib import Path

from app.config import OUTPUTS_DIR


def _path_for(video_id: str) -> Path:
    return OUTPUTS_DIR / f"{video_id}.json"


def save_transcript(video_id: str, language: str, segments: list[dict]) -> None:
    payload = {"video_id": video_id, "language": language, "segments": segments}
    _path_for(video_id).write_text(json.dumps(payload), encoding="utf-8")


def load_transcript(video_id: str) -> dict | None:
    path = _path_for(video_id)
    if not path.exists():
        return None
    return json.loads(path.read_text(encoding="utf-8"))


def update_segment(video_id: str, segment_index: int, *, text: str | None, start: float | None, end: float | None) -> dict | None:
    transcript = load_transcript(video_id)
    if transcript is None:
        return None
    if segment_index < 0 or segment_index >= len(transcript["segments"]):
        return None

    segment = transcript["segments"][segment_index]
    if text is not None:
        segment["text"] = text
    if start is not None:
        segment["start"] = start
    if end is not None:
        segment["end"] = end

    save_transcript(video_id, transcript["language"], transcript["segments"])
    return transcript
