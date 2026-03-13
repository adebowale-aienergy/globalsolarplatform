from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Dict

import joblib
import pandas as pd

from api.services.feature_store import FeatureStore


class ModelService:
    def __init__(self, model_path: Path, metadata_path: Path, feature_store: FeatureStore):
        self.model_path = model_path
        self.metadata_path = metadata_path
        self.feature_store = feature_store
        self.model = None
        self.model_loaded = False
        self.load_error: str | None = None
        self.version = "1.0.0"
        self.metadata: Dict[str, Any] = {}

    def load(self) -> None:
        self._load_metadata()
        try:
            self.model = joblib.load(self.model_path)
            self.model_loaded = True
            self.load_error = None
        except Exception as exc:
            self.model = None
            self.model_loaded = False
            self.load_error = str(exc)

    def _load_metadata(self) -> None:
        if self.metadata_path.exists():
            try:
                self.metadata = json.loads(self.metadata_path.read_text(encoding="utf-8"))
                self.version = self.metadata.get("version", self.version)
            except Exception:
                self.metadata = {}

    def health(self) -> dict:
        return {
            "model_loaded": self.model_loaded,
            "feature_count": len(self.feature_store.get_feature_columns()),
            "load_error": self.load_error,
        }

    def predict(self, features: Dict[str, Any]) -> dict:
        if not self.model_loaded or self.model is None:
            raise RuntimeError(
                "Model is not loaded. Check model compatibility or resave the joblib file."
            )

        missing, _ = self.feature_store.validate_features(features)
        if missing:
            raise ValueError(f"Missing required features: {missing}")

        ordered = {
            col: features[col]
            for col in self.feature_store.get_feature_columns()
        }
        frame = pd.DataFrame([ordered])
        prediction = self.model.predict(frame)[0]

        return {
            "prediction": float(prediction),
            "target": "target_GHI_next_day",
            "unit": "W/m²",
            "used_features": self.feature_store.get_feature_columns(),
        }
