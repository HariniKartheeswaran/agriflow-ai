import random
from agents.state import AgentState

def forecast_demand(state: AgentState):
    demand = state.get("demand", 100)
    stock = state.get("stock", 100)
    weather = state.get("weather", "").lower()
    
    # Advanced: Weather directly impacts stock availability and demand predictability!
    weather_multiplier = 1.0
    if "rain" in weather or "storm" in weather or "thunder" in weather:
        weather_multiplier = 0.6  # Heavy destruction to logistics / crop availability
    elif "clouds" in weather or "haze" in weather or "mist" in weather:
        weather_multiplier = 0.9  # Mild disruption
    elif "clear" in weather or "sun" in weather:
        weather_multiplier = 1.1  # Excellent yield, slight boost
        
    # Apply weather punishment/boost to stock
    adjusted_stock = int(stock * weather_multiplier)
    
    # Forecast fluctuates randomly as usual
    fluctuation = random.uniform(0.8, 1.2)
    
    return {
        "forecast": int(demand * fluctuation),
        "stock": adjusted_stock # updated stock!
    }