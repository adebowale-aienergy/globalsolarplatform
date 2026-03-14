import streamlit as st

from apps.api_client import get_api_health

st.title("API Access")

if st.button("Check API Health", type="primary"):
    try:
        result = get_api_health()
        st.success("API reachable")
        st.json(result)
    except Exception as exc:
        st.error(f"API check failed: {exc}")

st.code("http://127.0.0.1:8000/docs", language="text")
