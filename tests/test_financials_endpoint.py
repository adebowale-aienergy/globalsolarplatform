from fastapi.testclient import TestClient

from api.main import app

client = TestClient(app)


def test_financials_analyze():
    response = client.post(
        "/api/v1/financials/analyze",
        json={
            "annual_energy_kwh": 30000,
            "tariff_per_kwh": 0.15,
            "system_cost": 25000,
            "annual_opex": 1000,
        },
    )
    assert response.status_code == 200
    body = response.json()
    assert "roi_percent" in body
