import subprocess
from pathlib import Path

from app.config import OUTPUTS_DIR


def _format_srt_timestamp(seconds: float) -> str:
    millis = round(seconds * 1000)
    hours, millis = divmod(millis, 3_600_000)
    minutes, millis = divmod(millis, 60_000)
    secs, millis = divmod(millis, 1000)
    return f"{hours:02d}:{minutes:02d}:{secs:02d},{millis:03d}"


def build_srt(segments: list[dict]) -> str:
    lines = []
    for index, segment in enumerate(segments, start=1):
        lines.append(str(index))
        start = _format_srt_timestamp(segment["start"])
        end = _format_srt_timestamp(segment["end"])
        lines.append(f"{start} --> {end}")
        lines.append(segment["text"])
        lines.append("")
    return "\n".join(lines)


def write_srt(video_id: str, segments: list[dict]) -> Path:
    srt_path = OUTPUTS_DIR / f"{video_id}.srt"
    srt_path.write_text(build_srt(segments), encoding="utf-8")
    return srt_path


def export_with_burned_subtitles(
    video_id: str, source_path: Path, segments: list[dict], *, is_audio: bool
) -> Path:
    srt_path = write_srt(video_id, segments)
    output_path = OUTPUTS_DIR / f"{video_id}_export.mp4"
    escaped_srt = str(srt_path).replace("\\", "\\\\").replace(":", "\\:")

    if is_audio:
        cmd = [
            "ffmpeg",
            "-y",
            "-f",
            "lavfi",
            "-i",
            "color=c=black:s=1280x720",
            "-i",
            str(source_path),
            "-vf",
            f"subtitles={escaped_srt}",
            "-shortest",
            "-c:v",
            "libx264",
            "-c:a",
            "aac",
            str(output_path),
        ]
    else:
        cmd = [
            "ffmpeg",
            "-y",
            "-i",
            str(source_path),
            "-vf",
            f"subtitles={escaped_srt}",
            "-c:v",
            "libx264",
            "-c:a",
            "copy",
            str(output_path),
        ]

    result = subprocess.run(cmd, capture_output=True, text=True)
    if result.returncode != 0:
        raise RuntimeError(f"ffmpeg fallo al exportar: {result.stderr[-2000:]}")

    return output_path
