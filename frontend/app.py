import streamlit as st
import requests
import pandas as pd
import pydeck as pdk
import os
import re

BACKEND_URL = os.getenv("BACKEND_URL", "http://localhost:8000/run")
N8N_WEBHOOK_URL = os.getenv("N8N_WEBHOOK_URL", "http://localhost:5678/webhook/run-agri-ai")
HISTORY_URL = os.getenv("HISTORY_URL", "http://localhost:8000/history")

st.set_page_config(page_title="AgriFlow AI", layout="wide", initial_sidebar_state="expanded")

# --- GEOGRAPHIC DATASET ---
COORDINATES = {
    "Thanjavur": [10.7867, 79.1378],
    "Salem": [11.6643, 78.1460],
    "Coimbatore": [11.0168, 76.9558],
    "Madurai": [9.9252, 78.1198],
    "Chennai": [13.0827, 80.2707],
    "Tiruchirappalli": [10.7905, 78.7047],
    "Vellore": [12.9165, 79.1325],
    "Erode": [11.3410, 77.7172],
    "Tirunelveli": [8.7139, 77.7567],
    "Dindigul": [10.3673, 77.9803],
    "Kanyakumari": [8.0883, 77.5385],
    "Tiruppur": [11.1085, 77.3411]
}

# --- SIDEBAR CONTROLS ---
with st.sidebar:
    st.header("⚙️ Control Panel")
    location = st.selectbox("📍 Select District", list(COORDINATES.keys()))
    email = st.text_input("✉️ Alert Destination Email")
    run_button = st.button("🚀 Run AI Analysis", use_container_width=True)
    
    st.markdown("---")
    st.markdown("### 🛰️ System Status")
    st.markdown("🟢 **Neural Interface:** Online")
    st.markdown("🟢 **Logic Router:** Connected")
    st.markdown("🟢 **Weather SatLink:** Synced")

# --- MAIN DASHBOARD TABS ---
st.title("🌾 AgriFlow AI")

tab_live, tab_history = st.tabs(["🔴 Live Simulation", "📈 Historical Risk Analytics"])

if run_button:
    if email == "":
        st.sidebar.warning("Please enter an email")
        st.stop()

    with tab_live:
        with st.spinner("🤖 Simulating Weather Impact and Asking AI..."):
            try:
                res = requests.post(BACKEND_URL, json={"location": location, "email": email}, timeout=15)
                res.raise_for_status()
                result = res.json()
            except requests.exceptions.RequestException as e:
                st.error(f"Failed to connect to backend: {e}")
                st.stop()
            except ValueError:
                st.error("Backend returned invalid JSON")
                st.stop()

            # Trigger n8n
            try:
                requests.post(N8N_WEBHOOK_URL, json=result, timeout=5)
            except requests.exceptions.RequestException:
                st.toast(f"Automation Webhook unreachable at {N8N_WEBHOOK_URL}", icon="⚠️")

            # 📊 Metrics + Weather
            col1, col2 = st.columns(2)
            
            with col2:
                st.subheader("🌦 Network Weather")
                weather_desc = result.get("weather", "Unknown")
                if "rain" in weather_desc.lower() or "storm" in weather_desc.lower():
                    st.error(f"🌧️ {weather_desc.title()} - Causes severe logistics reduction.")
                else:
                    st.info(f"🌤️ {weather_desc.title()} - Logistics stable.")

                st.subheader("⚠️ Computed Risk Factor")
                risk_level = result.get("risk", "UNKNOWN")

                if risk_level == "HIGH_STOCKOUT_RISK":
                    st.error("🚨 Critical Stockout Imminent")
                elif risk_level == "OVERSTOCK_RISK":
                    st.warning("⚠️ High Depreciation / Overstock Risk")
                elif risk_level == "MEDIUM_RISK":
                    st.warning("⚠️ Medium Stock Strain (Monitor)")
                elif risk_level == "BALANCED":
                    st.success("✅ Ecosystem Balanced")
                else:
                    st.info(f"Risk Level: {risk_level}")

            with col1:
                st.subheader("📊 Physics & Metrics")
                df = pd.DataFrame({
                    "Metric": ["Initial Demand","Forecasted Shift","Available Stock","Personnel"],
                    "Value": [
                        result.get("demand", 0),
                        result.get("forecast", 0),
                        result.get("stock", 0),
                        result.get("staff", 0)
                    ]
                })
                st.bar_chart(df.set_index("Metric"), color="#3b82f6")

            # 🧠 Decision Engine
            decision_text = result.get("decision", "")
            decision_text = re.sub(r'\*\*(.*?)\*\*', r'<b>\1</b>', decision_text)
            decision_text = decision_text.replace("\n", "<br>")

            st.markdown(f"""
            <div style="background-color:#0f172a; padding:20px; border-radius:12px; border:1px solid #334155; line-height:1.7; font-size:16px;">
                <h3 style='margin-top:0px;'>🧠 AI Neural Recommendation</h3>
                {decision_text}
            </div>
            """, unsafe_allow_html=True)

            # 📍 Map Space
            st.divider()
            st.subheader(f"📍 Geographic Node Mapping: {location}")
            center_lat, center_lon = COORDINATES.get(location, [11, 78])

            if risk_level == "HIGH_STOCKOUT_RISK": color = [220, 38, 38, 200]
            elif risk_level == "OVERSTOCK_RISK": color = [234, 179, 8, 200]
            elif risk_level == "MEDIUM_RISK": color = [249, 115, 22, 200]
            else: color = [34, 197, 94, 200]

            import numpy as np
            conf = float(result.get("confidence", 0.0))
            np.random.seed(int(conf * 100)) 
            map_data = pd.DataFrame({
                "lat": np.random.normal(center_lat, 0.04, 5),
                "lon": np.random.normal(center_lon, 0.04, 5),
                "demand": np.random.normal(result.get("forecast", 100), 20, 5)
            })

            st.pydeck_chart(pdk.Deck(
                initial_view_state=pdk.ViewState(latitude=center_lat, longitude=center_lon, zoom=9, pitch=45),
                tooltip={"text": "Demographic Node\nPredicted Demand: {demand}"},
                layers=[
                    pdk.Layer(
                        "ColumnLayer",
                        data=map_data,
                        get_position='[lon, lat]',
                        get_elevation='demand',
                        elevation_scale=50,
                        radius=2000,
                        get_fill_color=str(color),
                        pickable=True, auto_highlight=True
                    )
                ],
            ))

# --- HISTORY TAB LOGIC ---
with tab_history:
    st.subheader(f"📈 Analytics Query: {location}")
    if st.button("Fetch Database History"):
        try:
            hist_res = requests.get(f"{HISTORY_URL}/{location}")
            history_data = hist_res.json().get("history", [])
            
            if len(history_data) == 0:
                st.info("No data simulated for this region yet.")
            else:
                st.success(f"Retrieved {len(history_data)} historical data points.")
                
                # Setup visualization DataFrame
                hist_df = pd.DataFrame([{
                    "Execution ID": i+1,
                    "Future Forecast": d.get("forecast", 0),
                    "Available Stock": d.get("stock", 0),
                    "Risk Matrix": d.get("risk", "UNKNOWN")
                } for i, d in enumerate(history_data)])
                
                st.line_chart(hist_df.set_index("Execution ID")[["Future Forecast", "Available Stock"]])
                st.dataframe(hist_df, use_container_width=True)
                
        except Exception as e:
            st.error(f"Failed to load history database: {e}")