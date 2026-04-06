# 🌱 AgriFlow AI: Intelligent Logistics & Supply Simulation

![License](https://img.shields.io/badge/license-MIT-blue.svg)
![Python](https://img.shields.io/badge/python-3.9%2B-blue)
![FastAPI](https://img.shields.io/badge/FastAPI-0.100%2B-00a393.svg)
![Streamlit](https://img.shields.io/badge/Streamlit-1.25%2B-FF4B4B.svg)
![n8n](https://img.shields.io/badge/n8n-Workflow_Automation-EA4B71.svg)

**AgriFlow AI** is an advanced, autonomous agricultural supply chain simulation platform. It uses real-time weather analytics, concurrent-safe memory management, and LangGraph-driven generative AI (via Groq/LLaMA-3) to predict dynamic geographic stockout risks and trigger autonomous webhooks for procurement automation.

---

## 🚀 Key Features

* **🧠 LLM-Driven Decision Engine**: Utilizes LLaMA-3.1 via Groq API to analyze regional demands, staffing, and weather implications to generate robust supply chain strategies.
* **🌩️ Real-Time Weather Physics**: Actively fetches OpenWeather API data. Storms, rain, and haze mathematically degrade inventory physics to simulate real-world logistics breakdowns.
* **📍 3D Interactive Geographic Mapping**: Built with PyDeck, the frontend dynamically maps user-selected Tamil Nadu districts, rendering towering 3D metrics corresponding exactly to local simulated demand.
* **⚡ Robust Backend Architecture**: Features a thread-safe, SQLite-backed memory layer engineered to completely eradicate race-conditions during high-volume API requests.
* **🤖 n8n Workflow Automation Engine**: Integrated directly with customized JSON payloads routing to advanced Ntfy.sh push-notifications and mock HTTP Auto-Procurement APIs.

---

## 🛠️ Tech Stack

* **Frontend:** Streamlit, Pandas, PyDeck, NumPy
* **Backend:** FastAPI, LangGraph, SQLite3, Pydantic
* **AI & external APIs:** Groq (LLaMA-3.1), OpenWeatherMap
* **Automation:** n8n, Ntfy.sh

---

## 📥 Installation

```bash
# Clone this repository
git clone https://github.com/yourusername/agriflow-ai.git
cd agriflow-ai

# Backend Setup
cd backend
python -m venv venv
venv\Scripts\activate  # Windows
pip install -r requirements.txt

# Frontend Setup
cd ../frontend
python -m venv venv
venv\Scripts\activate  # Windows
pip install -r requirements.txt
```

---

## ⚙️ Environment Configuration

You must create a `.env` file in the `backend/` directory:

```env
GROQ_API_KEY=your_groq_api_key_here
WEATHER_API_KEY=your_openweathermap_api_key_here
```

---

## 🏃 Execution

1. **Start the API Backend Server:**
   ```bash
   cd backend
   uvicorn main:app --port 8000 --reload
   ```

2. **Start the Streamlit Dashboard:**
   ```bash
   cd frontend
   streamlit run app.py --server.port 8501
   ```

3. **Deploy the Automation Engine (Optional):**
   * Start `npx n8n`
   * Import the `advanced-workflow.json` located in the `n8n/` folder.


