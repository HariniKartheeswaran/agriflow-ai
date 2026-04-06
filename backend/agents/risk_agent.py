from agents.state import AgentState

def assess_risk(state: AgentState):
    stock = state.get("stock", 50)
    forecast = state.get("forecast", 100)
    
    if forecast == 0:
        ratio = stock
    else:
        ratio = stock / forecast

    if ratio < 0.5:
        risk = "HIGH_STOCKOUT_RISK"
    elif ratio < 0.9:
        risk = "MEDIUM_RISK"
    elif ratio > 1.4:
        risk = "OVERSTOCK_RISK"
    else:
        risk = "BALANCED"

    alert_val = "⚠️ Immediate restocking required!" if risk == "HIGH_STOCKOUT_RISK" else None
    
    if alert_val:
        return {"risk": risk, "alert": alert_val}
    return {"risk": risk}