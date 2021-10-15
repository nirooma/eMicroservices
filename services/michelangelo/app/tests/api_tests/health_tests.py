from fastapi.testclient import TestClient
from main import app

client = TestClient(app)


def test_ping():
    response = client.get('/health')
    assert response.status_code == 200
