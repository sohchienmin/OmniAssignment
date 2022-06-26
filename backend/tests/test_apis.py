from fastapi.testclient import TestClient

from app.api.api import app

client = TestClient(app)

headers = {"accept": "application/json", "Content-Type": "application/json"}


def test_docs():
    response = client.get("/docs")
    assert response.status_code == 200


def test_generate_url():
    response = client.post(
        "/generate_url", headers=headers, json={"url": "https://google.com"}
    )
    assert response.status_code == 200


def test_generate_url_with_invalid_url():
    response = client.post(
        "/generate_url",
        headers=headers,
        json={"url": "https://thiswebsitedoesnotexistatall.com"},
    )
    assert response.status_code == 422


def test_generate_url_with_empty_url():
    response = client.post("/generate_url", headers=headers, json={"url": ""})
    assert response.status_code == 422


def test_generate_url_with_whitespace_url():
    response = client.post("/generate_url", headers=headers, json={"url": "     "})
    assert response.status_code == 422


def test_get_url_with_fake_key():
    response = client.get("/fakekey")
    assert response.status_code == 404
