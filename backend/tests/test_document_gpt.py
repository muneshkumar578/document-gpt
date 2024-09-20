from fastapi.testclient import TestClient
from app.main import api

def test_document_query_invalid_body_should_return_422():
    with TestClient(api) as client:
        response = client.post("/query", json={})
        assert response.status_code == 422

def test_document_query_valid_body_should_return_200():
    with TestClient(api) as client:
        response = client.post("/query", json={"query": "What are the standard work hours in ABC Inc.?", "thread_id": ""})
        assert response.status_code == 200

# ToDo: Add more tests