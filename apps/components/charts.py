import streamlit as st


def metric_card(label: str, value: str):
    st.metric(label=label, value=value)
