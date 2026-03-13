from pathlib import Path
from typing import List

from pydantic_settings import BaseSettings, SettingsConfigDict


BASE_DIR = Path(__file__).resolve().parent.parent


class Settings(BaseSettings):
    app_name: str = "Global Solar Platform API"
    app_version: str = "1.0.0"
    debug: bool = True
    api_prefix: str = "/api/v1"

    host: str = "0.0.0.0"
    port: int = 8000

    model_path: Path = BASE_DIR / "models" / "ghi_model.joblib"
    model_metadata_path: Path = BASE_DIR / "models" / "model_metadata.json"

    raw_data_path: Path = BASE_DIR / "data" / "Global_Solar_Data_2024.csv"
    clean_data_path: Path = BASE_DIR / "data" / "Global_Clean_Data_2024.csv"
    feature_data_path: Path = BASE_DIR / "data" / "Global_Feature_Data_2024.csv"

    allowed_origins: List[str] = ["*"]

    nasa_power_url: str = "https://power.larc.nasa.gov/api/temporal/daily/point"
    default_nasa_start: str = "20240101"
    default_nasa_end: str = "20240101"

    request_timeout_seconds: int = 30

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )


settings = Settings()
