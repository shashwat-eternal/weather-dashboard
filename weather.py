import requests
import pandas as pd


def get_coordinates(city):
    url = f"https://geocoding-api.open-meteo.com/v1/search?name={city}&count=1"

    response = requests.get(url)

    if response.status_code != 200:
        return None

    data = response.json()

    if "results" not in data:
        return None

    result = data["results"][0]

    return {
        "latitude": result["latitude"],
        "longitude": result["longitude"],
        "name": result["name"],
        "country": result["country"]
    }


def get_weather(city):

    location = get_coordinates(city)

    if not location:
        return None

    lat = location["latitude"]
    lon = location["longitude"]

    url = (
        f"https://api.open-meteo.com/v1/forecast?"
        f"latitude={lat}"
        f"&longitude={lon}"
        f"&current=temperature_2m,relative_humidity_2m,wind_speed_10m"
        f"&daily=temperature_2m_max,temperature_2m_min"
        f"&forecast_days=7"
        f"&timezone=auto"
    )

    response = requests.get(url)

    if response.status_code != 200:
        return None

    weather_data = response.json()

    return {
        "location": location,
        "current": weather_data["current"],
        "daily": weather_data["daily"]
    }


def forecast_dataframe(daily):

    df = pd.DataFrame({
        "Date": daily["time"],
        "Max Temp": daily["temperature_2m_max"],
        "Min Temp": daily["temperature_2m_min"]
    })

    return df