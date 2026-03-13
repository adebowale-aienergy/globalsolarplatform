from api.schemas import ReportRequest


class ReportService:
    def generate(self, payload: ReportRequest) -> dict:
        return {
            "site_name": payload.site_name,
            "coordinates": {
                "latitude": payload.latitude,
                "longitude": payload.longitude,
            },
            "forecast": payload.forecast.model_dump(),
            "production": payload.production.model_dump(),
            "financials": payload.financials.model_dump(),
            "summary": {
                "predicted_next_day_ghi": payload.forecast.prediction,
                "annual_energy_kwh": payload.production.annual_energy_kwh,
                "roi_percent": payload.financials.roi_percent,
                "payback_years": payload.financials.payback_years,
            },
        }
