from typing import Any, Dict

import requests

from api.config import settings


def fetch_nasa_power_data(
    latitude: float,
    longitude: float,
    start: str | None = None,
    end: str | None = None,
) -> Dict[str, Any]:
    params = {
        "parameters": "ALLSKY_SFC_SW_DWN,T2M,WS2M,RH2M,PRECTOTCORR",
        "community": "RE",
        "longitude": longitude,
        "latitude": latitude,
        "start": start or settings.default_nasa_start,
        "end": end or settings.default_nasa_end,
        "format": "JSON",
    }

    response = requests.get(
        settings.nasa_power_url,
        params=params,
        timeout=settings.request_timeout_seconds,
    )
    response.raise_for_status()

    data = response.json()["properties"]["parameter"]
    date_key = start or settings.default_nasa_start

    return {
        "GHI": data["ALLSKY_SFC_SW_DWN"].get(date_key),
        "temperature": data["T2M"].get(date_key),
        "wind_speed": data["WS2M"].get(date_key),
        "humidity": data["RH2M"].get(date_key),
        "precipitation": data["PRECTOTCORR"].get(date_key),
    }
