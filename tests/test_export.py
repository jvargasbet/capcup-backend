from app.services import export as export_service
from app.services.transcript_store import save_transcript


def test_build_srt_formats_timestamps_and_text():
    segments = [
        {"start": 0.0, "end": 1.5, "text": "Hola a todos"},
        {"start": 1.5, "end": 63.25, "text": "bienvenidos al editor"},
    ]
    srt = export_service.build_srt(segments)

    assert "1\n00:00:00,000 --> 00:00:01,500\nHola a todos" in srt
    assert "2\n00:00:01,500 --> 00:01:03,250\nbienvenidos al editor" in srt


def test_export_returns_404_without_transcript(client, uploaded_video_id):
    response = client.post(f"/videos/{uploaded_video_id}/export")
    assert response.status_code == 400


def test_export_calls_ffmpeg_and_returns_file(client, uploaded_video_id, monkeypatch):
    save_transcript(uploaded_video_id, "es", [{"start": 0.0, "end": 1.0, "text": "hola"}])

    def fake_export(video_id, source_path, segments, *, is_audio):
        output_path = export_service.OUTPUTS_DIR / f"{video_id}_export.mp4"
        output_path.write_bytes(b"fake-rendered-video")
        return output_path

    monkeypatch.setattr(
        "app.routers.videos.export_with_burned_subtitles", fake_export
    )

    response = client.post(f"/videos/{uploaded_video_id}/export")
    assert response.status_code == 200
    assert response.content == b"fake-rendered-video"
