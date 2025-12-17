import pandas as pd
import json
import os
from datetime import datetime

INPUT_FILE = "data/eurusd_5m_indicators.csv"
OUTPUT_DIR = "results"
OUTPUT_FILE = os.path.join(OUTPUT_DIR, "trend_status.json")

os.makedirs(OUTPUT_DIR, exist_ok=True)

# --- Load data ---
df = pd.read_csv(INPUT_FILE, parse_dates=["Datetime"])

# Seguridad básica
if len(df) < 60:
    raise ValueError("Not enough data to determine trend")

# Última vela
last = df.iloc[-1]

ema20 = last["EMA_20"]
ema50 = last["EMA_50"]
price = last["Close"]

# Umbral para evitar ruido (en pips)
THRESHOLD = 0.00005  # ~0.5 pip

if ema20 > ema50 + THRESHOLD:
    trend = "BULLISH"
elif ema20 < ema50 - THRESHOLD:
    trend = "BEARISH"
else:
    trend = "NEUTRAL"

result = {
    "timestamp": last["Datetime"].isoformat(),
    "price": round(price, 5),
    "ema20": round(ema20, 5),
    "ema50": round(ema50, 5),
    "trend": trend,
    "updated_utc": datetime.utcnow().isoformat()
}

with open(OUTPUT_FILE, "w") as f:
    json.dump(result, f, indent=2)

print("Trend detected:", result)
