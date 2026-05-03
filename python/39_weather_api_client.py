# ============================================================
# Program Title : Weather API Client (Open-Meteo – free, no key)
# Author        : Lydia S. Makiwa
# Date          : 2026-05-03
# Description   : Fetches real-time weather data for any city
#                 using Open-Meteo geocoding + forecast APIs.
# ============================================================

import requests

def get_coordinates(city: str) -> tuple:
    """Return (lat, lon, display_name) for a city name."""
    url  = "https://geocoding-api.open-meteo.com/v1/search"
    resp = requests.get(url, params={"name": city, "count": 1}, timeout=10)
    resp.raise_for_status()
    results = resp.json().get("results", [])
    if not results:
        raise ValueError(f"City '{city}' not found.")
    r = results[0]
    return r["latitude"], r["longitude"], r["name"] + ", " + r.get("country", "")

def get_weather(lat: float, lon: float) -> dict:
    """Return current weather data for the given coordinates."""
    url    = "https://api.open-meteo.com/v1/forecast"
    params = {
        "latitude":        lat,
        "longitude":       lon,
        "current_weather": True,
        "hourly":          "relativehumidity_2m,apparent_temperature",
        "forecast_days":   1,
    }
    resp = requests.get(url, params=params, timeout=10)
    resp.raise_for_status()
    return resp.json()

def wmo_description(code: int) -> str:
    """Convert WMO weather code to human-readable description."""
    codes = {
        0:"Clear sky", 1:"Mainly clear", 2:"Partly cloudy", 3:"Overcast",
        45:"Fog", 48:"Icy fog", 51:"Light drizzle", 61:"Slight rain",
        63:"Moderate rain", 65:"Heavy rain", 71:"Slight snow", 73:"Moderate snow",
        80:"Slight showers", 81:"Moderate showers", 95:"Thunderstorm",
    }
    return codes.get(code, f"Code {code}")

# ── Demo: fetch weather for multiple cities ───────────────────
cities = ["London", "Nairobi", "Tokyo"]

for city in cities:
    try:
        lat, lon, name = get_coordinates(city)
        data    = get_weather(lat, lon)
        current = data["current_weather"]
        humidity = data["hourly"]["relativehumidity_2m"][0]
        feels   = data["hourly"]["apparent_temperature"][0]

        print(f"🌍 {name}")
        print(f"   Temperature  : {current['temperature']}°C  (feels like {feels}°C)")
        print(f"   Wind speed   : {current['windspeed']} km/h")
        print(f"   Condition    : {wmo_description(current['weathercode'])}")
        print(f"   Humidity     : {humidity}%")
        print()
    except Exception as e:
        print(f"  Error for {city}: {e}")
