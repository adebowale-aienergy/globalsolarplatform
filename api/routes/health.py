from fastapi import APIRouter, Depends

from api.config import settings
from api.deps import get_model_service
from api.schemas import HealthResponse
from api.services.model_service import ModelService

router = APIRouter(tags=["Health"])


@router.get("/health", response_model=HealthResponse)
def health(service: ModelService = Depends(get_model_service)):
    status = service.health()
    return HealthResponse(
        service="api",
        version=settings.app_version,
        model_loaded=status["model_loaded"],
        feature_count=status["feature_count"],
        load_error=status["load_error"],
    )
