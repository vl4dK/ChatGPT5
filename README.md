# **ML Trading Bot**  
_Everyday-adaptive 1H/4H cryptocurrency trading bot with machine learning and risk management._

## 📌 Overview  
This project is a **Python-based algorithmic trading bot** that adapts daily to market conditions using machine learning models (LightGBM/XGBoost, optional River for online learning).  
It supports realistic execution with commissions and slippage, and includes a web-based GUI & API for monitoring and control.

**Time zone:** Europe/Amsterdam.

---

## 🚀 Key Features
- **Multi-timeframe trading:** 1H & 4H with candle-close synchronization.
- **Daily model retraining:** Walk-forward / purged split.
- **Advanced labeling:** Triple-barrier, forward returns, meta-labeling.
- **Risk management:** Volatility targeting, drawdown limits, ATR-based stops.
- **Execution engine:** Realistic slippage, fees, and latency.
- **Data orchestration:** Prefect/Airflow with DST/holidays handling.
- **Monitoring:** Prometheus + Grafana dashboards with Telegram alerts.

---

## 🛠 Tech Stack
- **Core:** Python 3.11, Poetry/uv, Docker
- **ML:** LightGBM, XGBoost, scikit-learn, mlflow
- **Data:** pandas, polars, numpy, ta
- **Backtesting:** vectorbt
- **Execution:** ccxt, optional Hyperliquid SDK
- **Orchestration:** Prefect, Airflow
- **Monitoring:** Prometheus, Grafana
- **API/GUI:** FastAPI, Streamlit

---

## 📂 Project Structure
```
.
├── README.md
├── ROADMAP.md
├── config.yaml
├── .env.example
├── pyproject.toml
├── docker-compose.yml
├── src/
│   ├── data/          # Data loaders & parquet storage
│   ├── features/      # Feature engineering
│   ├── labeling/      # Target labeling
│   ├── models/        # Training & prediction
│   ├── policy/        # Risk & position sizing
│   ├── exec/          # Order execution
│   ├── backtest/      # Backtesting engine
│   ├── orchestration/ # Task scheduling
│   ├── monitoring/    # Metrics & alerts
│   └── utils/         # Helper functions
├── api/               # FastAPI backend
└── ui/                # Streamlit dashboard
```

---

## ⚡ Quick Start

### 1️⃣ Install dependencies
```bash
# Using uv or Poetry
uv pip install -r requirements.txt || true
poetry install || true
```

### 2️⃣ Configure environment
Copy `.env.example` to `.env` and adjust settings.

### 3️⃣ Initialize data storage
```bash
python -m src.data.bootstrap --config config.yaml
```

### 4️⃣ Run bot workflows
```bash
# Daily retraining
python -m src.orchestration.run --flow daily_retrain

# Live decisions
python -m src.orchestration.run --flow live_decisions
```

### 5️⃣ Optional: Start monitoring
```bash
docker compose up -d prometheus grafana
```

---

## 🌐 API & GUI

- **API (FastAPI)** — Manage bot (start/stop, status, positions, trades)
```bash
uvicorn api.main:app --reload --port 8000
```

- **GUI (Streamlit)** — Live PnL/trades dashboard
```bash
streamlit run ui/dashboard.py
```
_Default API endpoint:_ `http://localhost:8000`  
_Custom API port:_  
```bash
BOT_API_URL=http://localhost:8001 streamlit run ui/dashboard.py
```

---

## 📊 Features & Targets
**Features:**  
- Returns, volatility, ATR, skew, kurtosis  
- Trend: EMA/SMA crossovers, RSI, Stoch, MACD, ADX  
- Volume: OBV, volume volatility, funding rates (perpetuals)  
- Multi-timeframe aggregation (1H → 4H)

**Targets:**  
- **Forward returns** (k bars ahead, net of fees)  
- **Triple-barrier** (Lopez de Prado method)  
- **Meta-labeling** (filtering weak signals)

---

## 📈 Validation
- Purged walk-forward split with embargo
- Metrics: CAGR, Sharpe, Sortino, Calmar, Max Drawdown
- Robustness: Stress-test for costs, latency, drift

---

## 🔒 Security
- API keys from `.env` / Vault
- Fail-safe: Close/hedge positions on failure
- Full audit trail: signal → decision → order → execution → PnL

---

## 📜 License
MIT (default) — or specify your own.
