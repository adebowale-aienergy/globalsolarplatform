import streamlit as st


def location_inputs():
    col1, col2 = st.columns(2)
    with col1:
        lat = st.number_input("Latitude", value=6.5244, format="%.6f")
    with col2:
        lon = st.number_input("Longitude", value=3.3792, format="%.6f")
    return lat, lon
