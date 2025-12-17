import pandas as pd
import numpy as np
import os

INPUT_FILE = "data/eurusd_5m.csv"
OUTPUT_FILE = "data/eurusd_5m_indicators.csv"

# --- load ---
df = pd.read_csv(INPUT_FILE)

# --- normaliza tiempo ---
df["Datetime"] = pd.to_datetime(df["Datetime"], utc=True)
df = df.drop_duplicates(subset=["Datetime"])
df = df.sort_values("Datetime").reset_index(drop=True)

# --- columnas numéricas obligatorias ---
PRICE_COLS = ["Open", "High", "Low", "Close"]

for col in PRICE_COLS:
    df[col] = pd.to_numeric(df[col], errors="coerce")

df = df.dropna(subset=PRICE_COLS)

# =========================
# INDICADORES
# =========================

# EMA
df["EMA_20"] = df["Close"].ewm(span=20, adjust=False).mean()
df["EMA_50"] = df["Close"].ewm(span=50, adjust=False).mean()

# RSI 14
delta = df["Close"].diff()
gain = delta.clip(lower=0)
loss = -delta.clip(upper=0)

avg_gain = gain.rolling(14).mean()
avg_loss = loss.rolling(14).mean()

rs = avg_gain / avg_loss
df["RSI_14"] = 100 - (100 / (1 + rs))

# Tendencia simple
df["trend"] = np.where(
    df["EMA_20"] > df["EMA_50"], "BULLISH", "BEARISH"
)

# --- limpia NaNs iniciales ---
df = df.dropna().reset_index(drop=True)

# --- guarda ---
os.makedirs("data", exist_ok=True)
df.to_csv(OUTPUT_FILE, index=False)

print("Indicators added successfully")
print(df.tail(5))
