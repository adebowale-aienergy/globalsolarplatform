import requests
import pandas as pd


BASE_URL = "https://power.larc.nasa.gov/api/temporal/daily/point"


def fetch_nasa_power(lat, lon, start="20240101", end="20241231"):

    params = {
        "parameters": "ALLSKY_SFC_SW_DWN,T2M,WS2M,RH2M,PRECTOTCORR",
        "community": "RE",
        "longitude": lon,
        "latitude": lat,
        "start": start,
        "end": end,
        "format": "JSON"
    }

    response = requests.get(BASE_URL, params=params)

    if response.status_code != 200:
        raise Exception("NASA POWER request failed")

    data = response.json()

    records = data["properties"]["parameter"]

    df = pd.DataFrame(records)

    df = df.T.reset_index()
    df.rename(columns={"index": "DATE"}, inplace=True)

    return df


if __name__ == "__main__":

    latitude = 6.5244
    longitude = 3.3792

    df = fetch_nasa_power(latitude, longitude)

    print(df.head())

    df.to_csv("data/nasa_power_sample.csv", index=False)

    print("Data saved to data/nasa_power_sample.csv")
