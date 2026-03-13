from api.schemas import ProductionRequest


class ProductionService:
    def simulate(self, payload: ProductionRequest) -> dict:
        dc_energy_kwh_day = (
            payload.ghi_kwh_m2_day
            * payload.panel_area_m2
            * payload.panel_efficiency
        )

        ac_energy_kwh_day = dc_energy_kwh_day * payload.performance_ratio
        annual_energy_kwh = ac_energy_kwh_day * 365

        capacity_factor_percent = None
        if payload.system_capacity_kw:
            capacity_factor_percent = (
                annual_energy_kwh / (payload.system_capacity_kw * 24 * 365)
            ) * 100

        return {
            "dc_energy_kwh_day": round(dc_energy_kwh_day, 3),
            "ac_energy_kwh_day": round(ac_energy_kwh_day, 3),
            "annual_energy_kwh": round(annual_energy_kwh, 3),
            "capacity_factor_percent": (
                round(capacity_factor_percent, 3)
                if capacity_factor_percent is not None
                else None
            ),
        }
