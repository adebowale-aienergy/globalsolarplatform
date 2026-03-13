from typing import Any, Dict, List, Optional

from pydantic import BaseModel, Field


class APIStatus(BaseModel):
    success: bool = True
    message: str = "OK"


class HealthResponse(APIStatus):
    service: str
    version: str
    model_loaded: bool
    feature_count: int
    load_error: Optional[str] = None


class ForecastRequest(BaseModel):
    features: Dict[str, Any] = Field(..., description="Model input features")


class ForecastFromLocationRequest(BaseModel):
    latitude: float
    longitude: float
    date: Optional[str] = None


class ForecastResponse(APIStatus):
    prediction: float
    target: str = "target_GHI_next_day"
    unit: str = "W/m²"
    used_features: List[str]


class ProductionRequest(BaseModel):
    ghi_kwh_m2_day: float = Field(..., gt=0)
    panel_area_m2: float = Field(..., gt=0)
    panel_efficiency: float = Field(..., gt=0, le=1)
    performance_ratio: float = Field(0.75, gt=0, le=1)
    system_capacity_kw: Optional[float] = Field(None, gt=0)


class ProductionResponse(APIStatus):
    dc_energy_kwh_day: float
    ac_energy_kwh_day: float
    annual_energy_kwh: float
    capacity_factor_percent: Optional[float] = None


class FinancialRequest(BaseModel):
    annual_energy_kwh: float = Field(..., gt=0)
    tariff_per_kwh: float = Field(..., gt=0)
    system_cost: float = Field(..., gt=0)
    annual_opex: float = Field(0.0, ge=0)


class FinancialResponse(APIStatus):
    annual_revenue: float
    annual_profit: float
    roi_percent: float
    payback_years: float


class ReportRequest(BaseModel):
    site_name: str
    latitude: float
    longitude: float
    forecast: ForecastResponse
    production: ProductionResponse
    financials: FinancialResponse


class ReportResponse(APIStatus):
    report: Dict[str, Any]


class ErrorResponse(BaseModel):
    detail: Any
