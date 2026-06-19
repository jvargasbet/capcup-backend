import pytest
from fastapi.testclient import TestClient

from app.main import app

TINY_MP4_BYTES = (
    b"\x00\x00\x00\x18ftypmp42\x00\x00\x00\x00mp42mp41"
    b"\x00\x00\x00\x08free\x00\x00\x00\x08mdat"
)


@pytest.fixture
def client():
    return TestClient(app)


@pytest.fixture
def uploaded_video_id(client):
    files = {"file": ("clip.mp4", TINY_MP4_BYTES, "video/mp4")}
    response = client.post("/videos/upload", files=files)
    assert response.status_code == 200
    return response.json()["video_id"]
