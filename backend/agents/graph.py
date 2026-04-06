from langgraph.graph import StateGraph
from agents.state import AgentState
from agents.weather_agent import get_weather
from agents.crop_agent import get_crop_data
from agents.inventory_agent import get_inventory
from agents.forecast_agent import forecast_demand
from agents.risk_agent import assess_risk
from agents.decision_agent import make_decision

def build_graph():
    g = StateGraph(AgentState)

    g.add_node("weather", get_weather)
    g.add_node("crop", get_crop_data)
    g.add_node("inventory", get_inventory)
    g.add_node("forecast", forecast_demand)
    g.add_node("risk", assess_risk)
    g.add_node("decision", make_decision)

    g.set_entry_point("weather")

    g.add_edge("weather", "crop")
    g.add_edge("crop", "inventory")
    g.add_edge("inventory", "forecast")
    g.add_edge("forecast", "risk")
    g.add_edge("risk", "decision")

    g.set_finish_point("decision")

    return g.compile()