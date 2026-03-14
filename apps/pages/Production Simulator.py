import streamlit as st

from apps.api_client import simulate_production
from apps.components.charts import metric_card

st.title("Production Simulator")

ghi_kwh_m2_day = st.number_input("GHI (kWh/m²/day)", value=5.5, min_value=0.1)
panel_area_m2 = st.number_input("Panel Area (m²)", value=100.0, min_value=0.1)
panel_efficiency = st.number_input("Panel Efficiency", value=0.20, min_value=0.01, max_value=1.0)
performance_ratio = st.number_input("Performance Ratio", value=0.75, min_value=0.01, max_value=1.0)
system_capacity_kw = st.number_input("System Capacity (kW)", value=20.0, min_value=0.1)

if st.button("Simulate Production", type="primary"):
    try:
        result = simulate_production(
            {
                "ghi_kwh_m2_day": ghi_kwh_m2_day,
                "panel_area_m2": panel_area_m2,
                "panel_efficiency": panel_efficiency,
                "performance_ratio": performance_ratio,
                "system_capacity_kw": system_capacity_kw,
            }
        )
        metric_card("AC Energy / Day", f"{result['ac_energy_kwh_day']:.2f} kWh")
        metric_card("Annual Energy", f"{result['annual_energy_kwh']:.2f} kWh")
        st.json(result)
    except Exception as exc:
        st.error(f"Simulation failed: {exc}")
