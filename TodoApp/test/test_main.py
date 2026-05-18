from fastapi.testclient import TestClient
from ..main import app
from fastapi import status

client = TestClient(app) # ana sunucuyu başlatmadan test için sahte bir client oluşturuyoruz


def test_return_health_check():
    response = client.get("/healthy")
    assert response.status_code == status.HTTP_200_OK
    assert response.json() == {'status': 'healthy'}