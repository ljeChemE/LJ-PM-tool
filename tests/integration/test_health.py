from app.main import app
from fastapi.testclient import TestClient


def test_health_reports_ok_when_database_is_reachable():
    client = TestClient(app)

    response = client.get("/health")

    assert response.status_code == 200
    assert response.json() == {"status": "ok"}
