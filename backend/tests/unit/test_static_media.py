from pathlib import Path

from fastapi.testclient import TestClient

from core.app import app


def test_media_is_served_with_api_root_path():
    image_path = Path(__file__).resolve().parents[2] / "media" / "images" / "a9fe3624-237a-4edb-9ed5-66cb9c7f0160.png"
    assert image_path.exists()

    response = TestClient(app).get(f"/api/v1/media/images/{image_path.name}")

    assert response.status_code == 200
    assert response.headers["content-type"] == "image/png"
