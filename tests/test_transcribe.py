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


def test_transcribe_is_cached_and_does_not_recompute(client, uploaded_video_id, monkeypatch):
    calls = []

    def fake_transcribe_audio(path: str):
        calls.append(path)
        return "es", [{"start": 0.0, "end": 1.0, "text": "hola"}]

    monkeypatch.setattr(transcribe_router, "transcribe_audio", fake_transcribe_audio)

    client.post(f"/videos/{uploaded_video_id}/transcribe")
    client.post(f"/videos/{uploaded_video_id}/transcribe")

    assert len(calls) == 1


def test_update_segment_edits_text_and_persists(client, uploaded_video_id, monkeypatch):
    def fake_transcribe_audio(path: str):
        return "es", [{"start": 0.0, "end": 1.2, "text": "hola a todos"}]

    monkeypatch.setattr(transcribe_router, "transcribe_audio", fake_transcribe_audio)
    client.post(f"/videos/{uploaded_video_id}/transcribe")

    response = client.patch(
        f"/videos/{uploaded_video_id}/transcript/0",
        json={"text": "hola a todas", "start": 0.1},
    )
    assert response.status_code == 200
    body = response.json()
    assert body["segments"][0]["text"] == "hola a todas"
    assert body["segments"][0]["start"] == 0.1
    assert body["segments"][0]["end"] == 1.2

    follow_up = client.post(f"/videos/{uploaded_video_id}/transcribe")
    assert follow_up.json()["segments"][0]["text"] == "hola a todas"


def test_update_segment_404_for_unknown_video(client):
    response = client.patch("/videos/does-not-exist/transcript/0", json={"text": "x"})
    assert response.status_code == 404


def test_update_segment_404_for_out_of_range_index(client, uploaded_video_id, monkeypatch):
    def fake_transcribe_audio(path: str):
        return "es", [{"start": 0.0, "end": 1.0, "text": "hola"}]

    monkeypatch.setattr(transcribe_router, "transcribe_audio", fake_transcribe_audio)
    client.post(f"/videos/{uploaded_video_id}/transcribe")

    response = client.patch(f"/videos/{uploaded_video_id}/transcript/5", json={"text": "x"})
    assert response.status_code == 404
