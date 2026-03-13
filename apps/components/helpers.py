import pandas as pd


def date_to_iso(date_value) -> str:
    return str(pd.to_datetime(date_value).date())
