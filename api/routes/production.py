from fastapi import APIRouter, Depends

from api.deps import get_production_service
from api.schemas import ProductionRequest, ProductionResponse
from api.services.production_service import ProductionService

router = APIRouter(prefix="/production", tags=["Production"])


@router.post("/simulate", response_model=ProductionResponse)
def simulate_production(
    payload: ProductionRequest,
    service: ProductionService = Depends(get_production_service),
):
    result = service.simulate(payload)
    return ProductionResponse(message="Production simulated", **result)
