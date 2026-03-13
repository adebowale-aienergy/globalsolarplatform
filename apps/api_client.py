import requests


API_BASE_URL = "http://127.0.0.1:8000/api/v1"


def get_api_health():
    response = requests.get(f"{API_BASE_URL}/health", timeout=30)
    response.raise_for_status()
    return response.json()


def predict_forecast(features: dict):
    response = requests.post(
        f"{API_BASE_URL}/forecast/predict",
        json={"features": features},
        timeout=60,
    )
    response.raise_for_status()
    return response.json()


def predict_forecast_from_location(latitude: float, longitude: float, date: str | None = None):
    payload = {"latitude": latitude, "longitude": longitude, "date": date}
    response = requests.post(
        f"{API_BASE_URL}/forecast/predict-from-location",
        json=payload,
        timeout=60,
    )
    response.raise_for_status()
    return response.json()


def simulate_production(payload: dict):
    response = requests.post(
        f"{API_BASE_URL}/production/simulate",
        json=payload,
        timeout=30,
    )
    response.raise_for_status()
    return response.json()


def analyze_financials(payload: dict):
    response = requests.post(
        f"{API_BASE_URL}/financials/analyze",
        json=payload,
        timeout=30,
    )
    response.raise_for_status()
    return response.json()


def generate_report(payload: dict):
    response = requests.post(
        f"{API_BASE_URL}/report/generate",
        json=payload,
        timeout=30,
    )
    response.raise_for_status()
    return response.json()
