from fastapi import FastAPI
from pydantic import BaseModel
from typing import Optional
from agents.graph import build_graph
from memory import save_memory

class RunRequest(BaseModel):
    location: str
    email: Optional[str] = None

app = FastAPI()
graph = build_graph()

@app.post("/run")
async def run_agents(request: RunRequest):
    input_data = request.model_dump(exclude_none=True)
    
    result = graph.invoke(input_data)
    
    result.setdefault("risk", "UNKNOWN")
    # Note: alert is natively set inside risk_agent
    
    save_memory(result)
    return result

import sqlite3
import json

@app.get("/history/{location}")
async def get_history(location: str):
    try:
        with sqlite3.connect("memory.db", timeout=10) as conn:
            conn.row_factory = sqlite3.Row
            rows = conn.execute("SELECT data FROM history ORDER BY id ASC").fetchall()
            
            history_data = []
            for row in rows:
                data = json.loads(row["data"])
                if data.get("location") == location:
                    history_data.append(data)
                    
            return {"history": history_data}
    except Exception as e:
        return {"history": []}