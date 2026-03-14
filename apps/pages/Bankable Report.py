import streamlit as st

from apps.api_client import generate_report

st.title("Bankable Report")

site_name = st.text_input("Site Name", value="Demo Solar Site")
latitude = st.number_input("Latitude", value=6.5244)
longitude = st.number_input("Longitude", value=3.3792)

st.caption("Paste or edit the JSON blocks below if you already ran Forecast, Production, and Financials.")

forecast_json = st.text_area(
    "Forecast JSON",
    value='{"success": true, "message": "Forecast generated", "prediction": 250.0, "target": "target_GHI_next_day", "unit": "W/m²", "used_features": []}',
    height=160,
)
production_json = st.text_area(
    "Production JSON",
    value='{"success": true, "message": "Production simulated", "dc_energy_kwh_day": 110.0, "ac_energy_kwh_day": 82.5, "annual_energy_kwh": 30112.5, "capacity_factor_percent": 17.19}',
    height=160,
)
financials_json = st.text_area(
    "Financials JSON",
    value='{"success": true, "message": "Financial analysis completed", "annual_revenue": 4516.88, "annual_profit": 3516.88, "roi_percent": 14.07, "payback_years": 7.11}',
    height=160,
)

if st.button("Generate Report", type="primary"):
    try:
        import json

        payload = {
            "site_name": site_name,
            "latitude": latitude,
            "longitude": longitude,
            "forecast": json.loads(forecast_json),
            "production": json.loads(production_json),
            "financials": json.loads(financials_json),
        }
        result = generate_report(payload)
        st.json(result)
    except Exception as exc:
        st.error(f"Report generation failed: {exc}")
