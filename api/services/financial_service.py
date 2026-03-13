from api.schemas import FinancialRequest


class FinancialService:
    def analyze(self, payload: FinancialRequest) -> dict:
        annual_revenue = payload.annual_energy_kwh * payload.tariff_per_kwh
        annual_profit = annual_revenue - payload.annual_opex
        roi_percent = (annual_profit / payload.system_cost) * 100
        payback_years = (
            payload.system_cost / annual_profit if annual_profit > 0 else float("inf")
        )

        return {
            "annual_revenue": round(annual_revenue, 2),
            "annual_profit": round(annual_profit, 2),
            "roi_percent": round(roi_percent, 2),
            "payback_years": round(payback_years, 2) if annual_profit > 0 else -1.0,
        }
