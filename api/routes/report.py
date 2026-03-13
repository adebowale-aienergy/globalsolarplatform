from fastapi import APIRouter, Depends

from api.deps import get_report_service
from api.schemas import ReportRequest, ReportResponse
from api.services.report_service import ReportService

router = APIRouter(prefix="/report", tags=["Report"])


@router.post("/generate", response_model=ReportResponse)
def generate_report(
    payload: ReportRequest,
    service: ReportService = Depends(get_report_service),
):
    result = service.generate(payload)
    return ReportResponse(message="Report generated", report=result)
