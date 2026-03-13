from __future__ import annotations

import math
from pathlib import Path
from typing import Any, Dict, Optional

import pandas as pd


class FeatureStore:
    def __init__(self, feature_csv_path: Path):
        self.feature_csv_path = feature_csv_path
        self.feature_columns = self._load_feature_columns()

    def _load_feature_columns(self) -> list[str]:
        df = pd.read_csv(self.feature_csv_path, nrows=1)
        return [col for col in df.columns if col != "target_GHI_next_day"]

    def get_feature_columns(self) -> list[str]:
        return self.feature_columns

    def build_time_features(self, date_value: str) -> Dict[str, Any]:
        dt = pd.to_datetime(date_value)
        day_of_year = int(dt.dayofyear)
        weekday = int(dt.weekday())
        return {
            "YEAR": int(dt.year),
            "MO": int(dt.month),
            "DY": int(dt.day),
            "DATE": str(dt.date()),
            "day_of_year": day_of_year,
            "month": int(dt.month),
            "weekday": weekday,
            "is_weekend": 1 if weekday >= 5 else 0,
            "sin_doy": math.sin(2 * math.pi * day_of_year / 365),
            "cos_doy": math.cos(2 * math.pi * day_of_year / 365),
        }

    def build_engineered_features(
        self,
        ghi: float,
        clearness_index: float,
        cloud_amount: float,
        ghi_lag_1: float,
        ghi_lag_3: float,
        ghi_lag_7: float,
    ) -> Dict[str, float]:
        roll_7 = (ghi + ghi_lag_1 + ghi_lag_3 + ghi_lag_7) / 4
        return {
            "GHI_roll_mean_3": (ghi + ghi_lag_1 + ghi_lag_3) / 3,
            "GHI_roll_mean_7": roll_7,
            "GHI_roll_mean_14": roll_7,
            "GHI_diff_1": ghi - ghi_lag_1,
            "clear_sky_proxy": ghi * clearness_index,
            "cloud_impact": 1 - (cloud_amount / 100),
        }

    def validate_features(self, payload: Dict[str, Any]) -> tuple[list[str], list[str]]:
        missing = [f for f in self.feature_columns if f not in payload]
        extra = [f for f in payload if f not in self.feature_columns]
        return missing, extra

    def build_minimal_location_features(
        self,
        latitude: float,
        longitude: float,
        date_value: Optional[str] = None,
    ) -> Dict[str, Any]:
        """
        Safe fallback for demo/testing when external weather data is not yet wired in.
        Replace with NASA POWER enrichment later.
        """
        date_value = date_value or "2024-06-15"
        time_features = self.build_time_features(date_value)

        ghi = 250.0
        clearness_index = 0.55
        cloud_amount = 45.0
        ghi_lag_1 = 245.0
        ghi_lag_3 = 238.0
        ghi_lag_7 = 220.0

        engineered = self.build_engineered_features(
            ghi=ghi,
            clearness_index=clearness_index,
            cloud_amount=cloud_amount,
            ghi_lag_1=ghi_lag_1,
            ghi_lag_3=ghi_lag_3,
            ghi_lag_7=ghi_lag_7,
        )

        features = {
            "YEAR": time_features["YEAR"],
            "MO": time_features["MO"],
            "DY": time_features["DY"],
            "Global Horizontal Irradiance (W/m²)": ghi,
            "Longwave Radiation (W/m²)": 320.0,
            "Clearness Index": clearness_index,
            "PAR Radiation (W/m²)": 110.0,
            "Air Temperature (°C)": 28.5,
            "Max Air Temperature (°C)": 32.0,
            "Min Air Temperature (°C)": 24.0,
            "Relative Humidity (%)": 75.0,
            "Precipitation (mm/day)": 1.2,
            "Wind Speed (m/s)": 3.5,
            "Wind Direction (°)": 180.0,
            "Surface Pressure (kPa)": 101.2,
            "Specific Humidity (g/kg)": 12.5,
            "Cloud Amount (%)": cloud_amount,
            "Latitude": latitude,
            "Longitude": longitude,
            "Country": "Unknown",
            "Region": "Unknown",
            "DATE": time_features["DATE"],
            "day_of_year": time_features["day_of_year"],
            "month": time_features["month"],
            "weekday": time_features["weekday"],
            "is_weekend": time_features["is_weekend"],
            "sin_doy": time_features["sin_doy"],
            "cos_doy": time_features["cos_doy"],
            "GHI_lag_1": ghi_lag_1,
            "GHI_lag_3": ghi_lag_3,
            "GHI_lag_7": ghi_lag_7,
            **engineered,
        }

        missing, _ = self.validate_features(features)
        if missing:
            raise ValueError(f"Feature generation incomplete. Missing: {missing}")

        return features
