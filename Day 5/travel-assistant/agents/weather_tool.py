from langchain.tools import tool
import requests

@tool
def get_weather(city: str) -> str:
    """Fetches current weather data for the given city."""
    url = f"http://wttr.in/{city}?format=3"
    response = requests.get(url)
    return response.text if response.status_code == 200 else "Weather data unavailable."

def get_weather_tool():
    return get_weather
