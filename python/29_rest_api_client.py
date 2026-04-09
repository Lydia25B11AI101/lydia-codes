# ============================================================
# Program Title : REST API Client with requests library
# Author        : Lydia S. Makiwa
# Date          : 2026-04-09
# Description   : Demonstrates calling public REST APIs.
#                 Fetches a programming joke, live weather
#                 (Open-Meteo), and GitHub user profile stats.
# ============================================================

import requests

def get_joke():
    """Fetch a random programming joke from a public API."""
    url = "https://official-joke-api.appspot.com/jokes/programming/random"
    try:
        r = requests.get(url, timeout=10)
        if r.status_code == 200:
            joke = r.json()[0]
            return joke['setup'] + "\n  -> " + joke['punchline']
    except Exception as e:
        return "Could not fetch joke: " + str(e)
    return "No joke today."

def get_weather(lat, lon, city):
    """Get current temperature using Open-Meteo (no API key required)."""
    url = (
        f"https://api.open-meteo.com/v1/forecast"
        f"?latitude={lat}&longitude={lon}&current_weather=true"
    )
    try:
        r = requests.get(url, timeout=10)
        if r.status_code == 200:
            cw = r.json()["current_weather"]
            return f"{city}: {cw['temperature']}C, wind {cw['windspeed']} km/h"
    except Exception as e:
        return f"{city}: unavailable ({e})"
    return f"{city}: no data"

def get_github_user(username):
    """Fetch public GitHub profile statistics."""
    try:
        r = requests.get(f"https://api.github.com/users/{username}", timeout=10)
        if r.status_code == 200:
            d = r.json()
            return (f"{d['login']} | Repos: {d['public_repos']} | "
                    f"Followers: {d['followers']}")
    except Exception as e:
        return f"Error: {e}"
    return "User not found."

# -- Demo --------------------------------------------------
if __name__ == "__main__":
    print("=" * 55)
    print("  REST API CLIENT DEMO — Lydia S. Makiwa")
    print("=" * 55)

    print("\n[1] Programming Joke:")
    print("  " + get_joke())

    print("\n[2] Live Weather:")
    cities = [
        (-25.7461, 28.1881, "Pretoria"),
        (51.5074,  -0.1278, "London"),
        (-26.2041, 28.0473, "Johannesburg"),
    ]
    for lat, lon, city in cities:
        print("  " + get_weather(lat, lon, city))

    print("\n[3] GitHub Stats:")
    for user in ["torvalds", "gvanrossum"]:
        print("  " + get_github_user(user))

    print("\nDone!")
