from data import get_mock_data
from agents.state import AgentState

def get_crop_data(state: AgentState):
    location = state.get("location", "Thanjavur")
    data = get_mock_data(location)
    return data