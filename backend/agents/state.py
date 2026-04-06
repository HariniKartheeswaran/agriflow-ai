from typing import TypedDict, Optional

class AgentState(TypedDict, total=False):
    location: str
    email: Optional[str]
    weather: Optional[str]
    crop: Optional[str]
    demand: Optional[int]
    stock: Optional[int]
    staff: Optional[int]
    forecast: Optional[int]
    risk: Optional[str]
    decision: Optional[str]
    confidence: Optional[float]
    alert: Optional[str]
