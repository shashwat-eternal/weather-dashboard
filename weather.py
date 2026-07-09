import requests
import pandas as pd

GEOCODE_URL = "https://geocoding-api.open-meteo.com/v1/search"
FORECAST_URL = "https://api.open-meteo.com/v1/forecast"


def get_location(city: str):
    params = {"name": city, "count": 1, "language": "en", "format": "json"}
    response = requests.get(GEOCODE_URL, params=params, timeout=20)
    response.raise_for_status()
    data = response.json()

    if "results" not in data or not data["results"]:
        return None

    result = data["results"][0]
    return {
        "name": result.get("name"),
        "country": result.get("country", ""),
        "latitude": result.get("latitude"),
        "longitude": result.get("longitude"),
        "timezone": result.get("timezone", "auto")
    }


def get_weather_data(latitude, longitude, timezone="auto"):
    params = {
        "latitude": latitude,
        "longitude": longitude,
        "timezone": timezone,
        "current": [
            "temperature_2m",
            "relative_humidity_2m",
            "apparent_temperature",
            "is_day",
            "precipitation",
            "weather_code",
            "surface_pressure",
            "wind_speed_10m",
            "wind_direction_10m"
        ],
        "hourly": [
            "temperature_2m",
            "relative_humidity_2m",
            "precipitation_probability",
            "wind_speed_10m"
        ],
        "daily": [
            "weather_code",
            "temperature_2m_max",
            "temperature_2m_min",
            "sunrise",
            "sunset",
            "precipitation_sum",
            "wind_speed_10m_max"
        ],
        "forecast_days": 7
    }

    response = requests.get(FORECAST_URL, params=params, timeout=20)
    response.raise_for_status()
    return response.json()


def weather_code_to_text(code: int):
    mapping = {
        0: "Clear sky",
        1: "Mainly clear",
        2: "Partly cloudy",
        3: "Overcast",
        45: "Fog",
        48: "Depositing rime fog",
        51: "Light drizzle",
        53: "Moderate drizzle",
        55: "Dense drizzle",
        56: "Freezing drizzle",
        57: "Dense freezing drizzle",
        61: "Slight rain",
        63: "Moderate rain",
        65: "Heavy rain",
        66: "Freezing rain",
        67: "Heavy freezing rain",
        71: "Slight snow",
        73: "Moderate snow",
        75: "Heavy snow",
        77: "Snow grains",
        80: "Rain showers",
        81: "Moderate rain showers",
        82: "Violent rain showers",
        85: "Slight snow showers",
        86: "Heavy snow showers",
        95: "Thunderstorm",
        96: "Thunderstorm with hail",
        99: "Severe thunderstorm with hail"
    }
    return mapping.get(code, "Unknown")


def weather_code_to_icon(code: int):
    if code == 0:
        return "☀️"
    if code in [1, 2]:
        return "🌤️"
    if code == 3:
        return "☁️"
    if code in [45, 48]:
        return "🌫️"
    if code in [51, 53, 55, 56, 57]:
        return "🌦️"
    if code in [61, 63, 65, 66, 67, 80, 81, 82]:
        return "🌧️"
    if code in [71, 73, 75, 77, 85, 86]:
        return "❄️"
    if code in [95, 96, 99]:
        return "⛈️"
    return "🌍"


def build_hourly_dataframe(weather_json):
    hourly = weather_json["hourly"]
    df = pd.DataFrame({
        "time": pd.to_datetime(hourly["time"]),
        "temperature": hourly["temperature_2m"],
        "humidity": hourly["relative_humidity_2m"],
        "rain_probability": hourly["precipitation_probability"],
        "wind_speed": hourly["wind_speed_10m"]
    })
    return df


def build_daily_dataframe(weather_json):
    daily = weather_json["daily"]
    df = pd.DataFrame({
        "date": pd.to_datetime(daily["time"]).date,
        "weather_code": daily["weather_code"],
        "max_temp": daily["temperature_2m_max"],
        "min_temp": daily["temperature_2m_min"],
        "precipitation_sum": daily["precipitation_sum"],
        "wind_speed_max": daily["wind_speed_10m_max"],
        "sunrise": daily["sunrise"],
        "sunset": daily["sunset"]
    })
    return df