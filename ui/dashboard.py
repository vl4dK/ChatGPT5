import os, time, requests, pandas as pd, streamlit as st

API_URL = os.getenv("BOT_API_URL", "http://localhost:8000")

st.set_page_config(page_title="ML Trading Bot", layout="wide")

st.title("📈 ML Trading Bot — Dashboard")

col1, col2, col3, col4 = st.columns(4)
status = requests.get(f"{API_URL}/status").json()
col1.metric("Running", str(status.get("running")))
col2.metric("Paper", str(status.get("paper")))
col3.metric("PnL", round(status.get("pnl", 0.0), 2))
col4.metric("Trades", status.get("trades", 0))
col4.metric("ASR", round(status.get("asr", 0.0), 2))


st.divider()

st.subheader("Execution Controls")
aggr = st.slider("Aggressiveness", min_value=0.0, max_value=1.0, step=0.05, value=0.5)
stress_mode = st.checkbox("Stress-test mode (simulate competitor bots)", value=False)
st.session_state["aggressiveness"] = aggr
st.session_state["stress_mode"] = stress_mode
st.caption(f"Aggressiveness = {aggr}, Stress mode = {stress_mode}")
st.divider()

c1, c2 = st.columns(2)
with c1:
    st.subheader("Control")
    start_paper = st.toggle("Paper trading", value=True, help="Вкл/выкл paper режим для старта")
    if st.button("▶️ Start bot"):
        r = requests.post(f"{API_URL}/start", json={"paper": start_paper})
        st.success(r.json())
    if st.button("⏹ Stop bot"):
        r = requests.post(f"{API_URL}/stop")
        st.success(r.json())

with c2:
    st.subheader("Positions / Metrics")
    pos = requests.get(f"{API_URL}/positions").json()
    st.json(pos)
    m = requests.get(f"{API_URL}/metrics").json()
    st.json(m)

st.divider()

st.subheader("Recent Orders & Trades")
orders = requests.get(f"{API_URL}/orders").json()
trades = requests.get(f"{API_URL}/trades").json()

if orders:
    st.write("Orders")
    st.dataframe(pd.DataFrame(orders))
if trades:
    st.write("Trades")
    st.dataframe(pd.DataFrame(trades))

st.caption("API_URL = {}".format(API_URL))
