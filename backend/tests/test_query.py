import sys
from pathlib import Path

from fastapi.testclient import TestClient


# Add the backend directory to Python's import path
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from app.main import app


def test_query_happy_path():

    with TestClient(app) as client:

        response = client.post(
            "/query",
            json={
                "question": "How do I charge the laptop?"
            }
        )

        assert response.status_code == 200

        data = response.json()

        assert "answer" in data
        assert "sources" in data

        assert isinstance(data["answer"], str)
        assert isinstance(data["sources"], list)


def test_query_invalid_input():

    with TestClient(app) as client:

        response = client.post(
            "/query",
            json={}
        )

        assert response.status_code == 422