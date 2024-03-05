from fastapi.testclient import TestClient
from main import app  # Using FastAPI app which is in a file named main.py

client = TestClient(app)


def test_add_book():
    response = client.post(
        "/books/",
        json={"title": "Test Book", "author": "Test Author", "publication_year": 2022},
    )
    assert response.status_code == 200
    assert response.json()["title"] == "Test Book"


def test_submit_review():
    response = client.post(
        "/reviews/",
        json={"book_id": 1, "text": "Great book!", "rating": 5},
    )
    assert response.status_code == 200
    assert response.json()["text"] == "Great book!"


def test_get_books():
    response = client.get("/books/")
    assert response.status_code == 200
    assert len(response.json()) > 0


def test_get_reviews():
    response = client.get("/reviews/1")
    assert response.status_code == 200
    assert len(response.json()) > 0
