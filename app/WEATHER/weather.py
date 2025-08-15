import os
import requests
from dotenv import load_dotenv

load_dotenv()

def get_weather_emoji(condition):
    """Map weather condition to emoji."""
    emoji_map = {
        "Clear": "☀️",
        "Clouds": "☁️",
        "Rain": "🌧️",
        "Snow": "❄️",
        "Thunderstorm": "⛈️",
        "Drizzle": "🌦️",
        "Mist": "🌫️",
        "Fog": "🌫️",
        "Haze": "🌫️",
        "Smoke": "💨",
        "Dust": "🌪️",
        "Sand": "🏜️",
        "Ash": "🌋",
        "Squall": "💨",
        "Tornado": "🌪️"
    }
    return emoji_map.get(condition, "🌈")  # Default fallback emoji


def get_weather(city_name, api_key=None):
    """Fetch weather data from OpenWeatherMap API."""
    if not api_key:
        api_key = os.getenv("OPEN_WEATHER_API")
    if not api_key:
        raise ValueError("API KEY MISSING")

    base_url = "https://api.openweathermap.org/data/2.5/weather"
    params = {
        "q": city_name,
        "appid": api_key,
        "units": "metric"
    }

    try:
        response = requests.get(base_url, params)
        response.raise_for_status()
        data = response.json()

        return {
            "city": data["name"],
            "temp": round(data["main"]["temp"]),
            "condition": data["weather"][0]["main"],
            "description": data["weather"][0]["description"],
            "feels_like": round(data["main"]["feels_like"]),
            "humidity": data["main"]["humidity"],
            "wind_speed": data["wind"]["speed"]
        }

    except requests.RequestException as e:
        print("Error:", e)
        return None


def run_weather_func(city):
    """Fetch and return weather data and emoji for the given city."""
    weather_data = get_weather(city)

    if not weather_data:
        print("⚠️ Failed to fetch weather.")
        return None

    emoji = get_weather_emoji(weather_data["condition"])

    return {
        **weather_data,
        "emoji": emoji
    }
