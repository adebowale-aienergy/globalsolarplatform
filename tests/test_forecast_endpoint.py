from fastapi.testclient import TestClient

from api.main import app

client = TestClient(app)


def test_forecast_health():
    response = client.get("/api/v1/forecast/health")
    assert response.status_code == 200


def test_forecast_from_location():
    response = client.post(
        "/api/v1/forecast/predict-from-location",
        json={"latitude": 6.5244, "longitude": 3.3792, "date": "2024-06-15"},
    )
    assert response.status_code in (200, 503)
