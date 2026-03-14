from fastapi.testclient import TestClient

from api.main import app

client = TestClient(app)


def test_production_simulate():
    response = client.post(
        "/api/v1/production/simulate",
        json={
            "ghi_kwh_m2_day": 5.5,
            "panel_area_m2": 100,
            "panel_efficiency": 0.2,
            "performance_ratio": 0.75,
            "system_capacity_kw": 20,
        },
    )
    assert response.status_code == 200
    body = response.json()
    assert "annual_energy_kwh" in body
