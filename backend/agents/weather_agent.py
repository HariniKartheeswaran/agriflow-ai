import requests, os
from agents.state import AgentState

def get_weather(state: AgentState):
    api_key = os.getenv("WEATHER_API_KEY")
    city = state.get("location", "Thanjavur")

    if not api_key:
        return {"weather": "unknown (No API Key)"}

    url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}"

    try:
        data = requests.get(url, timeout=5).json()
        weather = data.get("weather", [{}])[0].get("description", "unknown")
    except:
        weather = "unknown (API Error)"

    return {"weather": weather}