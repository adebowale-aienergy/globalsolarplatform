import streamlit as st

from apps.api_client import analyze_financials
from apps.components.charts import metric_card

st.title("Financial Analysis")

annual_energy_kwh = st.number_input("Annual Energy (kWh)", value=30000.0, min_value=1.0)
tariff_per_kwh = st.number_input("Tariff per kWh", value=0.15, min_value=0.0001)
system_cost = st.number_input("System Cost", value=25000.0, min_value=1.0)
annual_opex = st.number_input("Annual OPEX", value=1000.0, min_value=0.0)

if st.button("Analyze Financials", type="primary"):
    try:
        result = analyze_financials(
            {
                "annual_energy_kwh": annual_energy_kwh,
                "tariff_per_kwh": tariff_per_kwh,
                "system_cost": system_cost,
                "annual_opex": annual_opex,
            }
        )
        metric_card("ROI", f"{result['roi_percent']:.2f}%")
        metric_card("Payback", f"{result['payback_years']:.2f} years")
        st.json(result)
    except Exception as exc:
        st.error(f"Financial analysis failed: {exc}")
