from pathlib import Path

from fastapi.testclient import TestClient

from core.app import app


def test_media_is_served_with_api_root_path():
    image_dir = Path(__file__).resolve().parents[2] / "media" / "images"
    image_dir.mkdir(parents=True, exist_ok=True)
    image_path = image_dir / "test-static-media.png"
    image_path.write_bytes(
        b"\x89PNG\r\n\x1a\n\x00\x00\x00\rIHDR\x00\x00\x00\x01"
        b"\x00\x00\x00\x01\x08\x06\x00\x00\x00\x1f\x15\xc4\x89"
        b"\x00\x00\x00\nIDATx\x9cc\x00\x01\x00\x00\x05\x00\x01"
        b"\r\n-\xb4\x00\x00\x00\x00IEND\xaeB`\x82"
    )

    try:
        response = TestClient(app).get(f"/api/v1/media/images/{image_path.name}")
    finally:
        image_path.unlink(missing_ok=True)

    assert response.status_code == 200
    assert response.headers["content-type"] == "image/png"
