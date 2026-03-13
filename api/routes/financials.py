from fastapi import APIRouter, Depends

from api.deps import get_financial_service
from api.schemas import FinancialRequest, FinancialResponse
from api.services.financial_service import FinancialService

router = APIRouter(prefix="/financials", tags=["Financials"])


@router.post("/analyze", response_model=FinancialResponse)
def analyze_financials(
    payload: FinancialRequest,
    service: FinancialService = Depends(get_financial_service),
):
    result = service.analyze(payload)
    return FinancialResponse(message="Financial analysis completed", **result)
