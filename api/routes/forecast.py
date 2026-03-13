from fastapi import APIRouter, Depends, HTTPException, status

from api.deps import get_feature_store, get_model_service
from api.schemas import (
    ForecastFromLocationRequest,
    ForecastRequest,
    ForecastResponse,
    HealthResponse,
)
from api.services.feature_store import FeatureStore
from api.services.model_service import ModelService

router = APIRouter(prefix="/forecast", tags=["Forecast"])


@router.get("/health", response_model=HealthResponse)
def forecast_health(service: ModelService = Depends(get_model_service)):
    status_payload = service.health()
    return HealthResponse(
        service="forecast",
        version=service.version,
        model_loaded=status_payload["model_loaded"],
        feature_count=status_payload["feature_count"],
        load_error=status_payload["load_error"],
    )


@router.post("/predict", response_model=ForecastResponse)
def predict_forecast(
    payload: ForecastRequest,
    service: ModelService = Depends(get_model_service),
):
    try:
        result = service.predict(payload.features)
        return ForecastResponse(message="Forecast generated", **result)
    except ValueError as exc:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail=str(exc),
        ) from exc
    except RuntimeError as exc:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail=str(exc),
        ) from exc


@router.post("/predict-from-location", response_model=ForecastResponse)
def predict_from_location(
    payload: ForecastFromLocationRequest,
    service: ModelService = Depends(get_model_service),
    feature_store: FeatureStore = Depends(get_feature_store),
):
    try:
        features = feature_store.build_minimal_location_features(
            latitude=payload.latitude,
            longitude=payload.longitude,
            date_value=payload.date,
        )
        result = service.predict(features)
        return ForecastResponse(message="Forecast generated from location", **result)
    except ValueError as exc:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail=str(exc),
        ) from exc
    except RuntimeError as exc:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail=str(exc),
        ) from exc
