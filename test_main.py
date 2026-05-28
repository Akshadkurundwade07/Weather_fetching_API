from fastapi.testclient import TestClient
from unittest.mock import patch, MagicMock
from main import app

client = TestClient(app)

MOCK_DATA = {
    "name": "Mumbai",
    "sys": {"country": "IN"},
    "weather": [{"description": "clear sky"}],
    "main": {"temp": 32.0, "feels_like": 35.0, "humidity": 70},
    "wind": {"speed": 5.0}
}

def test_home():
    r = client.get("/")
    assert r.status_code == 200

def test_health():
    r = client.get("/health")
    assert r.json()["status"] == "ok"

def test_get_weather():
    mock_response = MagicMock()
    mock_response.status_code = 200
    mock_response.json.return_value = MOCK_DATA

    with patch("httpx.AsyncClient.get", return_value=mock_response):
        r = client.get("/weather/Mumbai")

    assert r.status_code == 200
    assert r.json()["city"] == "Mumbai"
    assert r.json()["temperature"] == 32.0