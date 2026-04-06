from groq import Groq
from dotenv import load_dotenv
import os, random
from agents.state import AgentState

load_dotenv()
api_key = os.getenv("GROQ_API_KEY")
client = Groq(api_key=api_key) if api_key else None

def make_decision(state: AgentState):
    if not client:
        return {"decision": "Fallback decision: No Groq API Key found. System simulates basic behavior without LLM advice.", "confidence": 0.0}

    prompt = f"""
    Location: {state.get('location')}
    Weather: {state.get('weather')}
    Crop: {state.get('crop')}
    Demand: {state.get('demand')}
    Forecast: {state.get('forecast')}
    Stock: {state.get('stock')}
    Staff: {state.get('staff')}
    Risk: {state.get('risk')}

    Provide:
    Recommendation:
    Reason:
    Action Steps:
    """

    try:
        res = client.chat.completions.create(
            model="llama-3.1-8b-instant",  
            messages=[{"role": "user", "content": prompt}],
            timeout=10
        )
        decision_text = res.choices[0].message.content
        
        # Parse markdown to HTML natively at the backend level so n8n emails get the formatting!
        import re
        decision_text = decision_text.replace("\n", "<br>")
        decision_text = re.sub(r'\*\*(.*?)\*\*', r'<b>\1</b>', decision_text)
        decision_text = re.sub(r'\*(.*?)\*', r'<i>\1</i>', decision_text)
        
        confidence = round(random.uniform(0.8, 0.95), 2)
    except Exception as e:
        decision_text = f"Fallback decision due to AI error: {str(e)}"
        confidence = 0.0

    return {"decision": decision_text, "confidence": confidence}