import pandas as pd
import json
import os
from datetime import datetime

DATA_FILE = "data/eurusd_5m_indicators.csv"
TREND_FILE = "results/trend_status.json"
OUTPUT_FILE = "results/entry_signal.json"

# --- Load data ---
df = pd.read_csv(DATA_FILE, parse_dates=["Datetime"])

if len(df) < 20:
    raise ValueError("Not enough data for RSI signal")

# Últimas dos velas
prev = df.iloc[-2]
last = df.iloc[-1]

rsi_prev = prev["RSI_14"]
rsi_now = last["RSI_14"]
price = last["Close"]

# --- Load trend ---
with open(TREND_FILE, "r") as f:
    trend_data = json.load(f)

trend = trend_data["trend"]

signal = "NONE"
direction = None

if trend == "BULLISH":
    if rsi_prev < 30 and rsi_now >= 30:
        signal = "ENTRY"
        direction = "LONG"

elif trend == "BEARISH":
    if rsi_prev > 70 and rsi_now <= 70:
        signal = "ENTRY"
        direction = "SHORT"

result = {
    "timestamp": last["Datetime"].isoformat(),
    "price": round(price, 5),
    "trend": trend,
    "rsi_prev": round(rsi_prev, 2),
    "rsi_now": round(rsi_now, 2),
    "signal": signal,
    "direction": direction,
    "updated_utc": datetime.utcnow().isoformat()
}

os.makedirs("results", exist_ok=True)
with open(OUTPUT_FILE, "w") as f:
    json.dump(result, f, indent=2)

print("Entry signal:", result)
