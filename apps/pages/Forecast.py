from datetime import date

import streamlit as st

from apps.api_client import predict_forecast_from_location
from apps.components.charts import metric_card
from apps.components.helpers import date_to_iso
from apps.components.maps import location_inputs

st.title("Forecast")

selected_date = st.date_input("Forecast date", value=date(2024, 6, 15))
lat, lon = location_inputs()

if st.button("Run Forecast", type="primary"):
    try:
        result = predict_forecast_from_location(
            latitude=lat,
            longitude=lon,
            date=date_to_iso(selected_date),
        )
        metric_card("Predicted Next-Day GHI", f"{result['prediction']:.2f} {result['unit']}")
        st.json(result)
    except Exception as exc:
        st.error(f"Forecast failed: {exc}")
