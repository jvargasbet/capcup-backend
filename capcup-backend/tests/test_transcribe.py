from app.routers import transcribe as transcribe_router


def test_transcribe_returns_segments_with_detected_speech(client, uploaded_video_id, monkeypatch):
    fake_segments = [
        {"start": 0.0, "end": 1.2, "text": "Hola a todos"},
        {"start": 1.2, "end": 3.4, "text": "bienvenidos al editor"},
    ]

    def fake_transcribe_audio(path: str):
        assert path
        return "es", fake_segments

    monkeypatch.setattr(transcribe_router, "transcribe_audio", fake_transcribe_audio)

    response = client.post(f"/videos/{uploaded_video_id}/transcribe")
    assert response.status_code == 200

    body = response.json()
    assert body["video_id"] == uploaded_video_id
    assert body["language"] == "es"
    assert body["segments"] == fake_segments


def test_transcribe_404_for_unknown_video(client):
    response = client.post("/videos/does-not-exist/transcribe")
    assert response.status_code == 404
