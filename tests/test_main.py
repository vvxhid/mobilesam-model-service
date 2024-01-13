from fastapi.testclient import TestClient
from fastapi import status
from app.main import app
from pathlib import Path


def test_segment_image():
    with TestClient(app) as client:
        with open(Path(__file__).parent / "resources/dog.jpg", "rb") as file:
            response = client.post(
                "/segment-image/",
                files={"file": ("test_image.png", file, "image/png")},
            )

            assert response.status_code == status.HTTP_200_OK
            assert response.headers["content-type"] == "image/png"


def test_segment_image_missing_file():
    with TestClient(app) as client:
        response = client.post(
            "/segment-image/",
            files={},
        )

        assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY
