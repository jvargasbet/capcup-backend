from app.config import UPLOADS_DIR


def test_upload_rejects_unsupported_extension(client):
    files = {"file": ("notes.txt", b"hello", "text/plain")}
    response = client.post("/videos/upload", files=files)
    assert response.status_code == 400


def test_upload_accepts_video_and_returns_id(client):
    files = {"file": ("clip.mp4", b"\x00\x00\x00\x18ftypmp42", "video/mp4")}
    response = client.post("/videos/upload", files=files)
    assert response.status_code == 200

    body = response.json()
    assert body["video_id"]
    assert body["filename"].endswith(".mp4")
    assert (UPLOADS_DIR / body["filename"]).exists()


def test_upload_accepts_audio_and_flags_is_audio(client):
    files = {"file": ("voice.mp3", b"ID3fake-audio-bytes", "audio/mpeg")}
    response = client.post("/videos/upload", files=files)
    assert response.status_code == 200

    body = response.json()
    assert body["is_audio"] is True
    assert body["filename"].endswith(".mp3")


def test_upload_accepts_video_and_flags_is_audio_false(client):
    files = {"file": ("clip.mp4", b"\x00\x00\x00\x18ftypmp42", "video/mp4")}
    response = client.post("/videos/upload", files=files)
    assert response.json()["is_audio"] is False


def test_get_video_file_returns_uploaded_bytes(client, uploaded_video_id):
    response = client.get(f"/videos/{uploaded_video_id}/file")
    assert response.status_code == 200
    assert response.content.startswith(b"\x00\x00\x00\x18ftyp")


def test_get_video_file_404_for_unknown_id(client):
    response = client.get("/videos/does-not-exist/file")
    assert response.status_code == 404
