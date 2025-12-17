import pandas as pd
import numpy as np
import os

INPUT_FILE = "data/eurusd_5m.csv"
OUTPUT_FILE = "data/eurusd_5m_indicators.csv"

# =========================
# LOAD
# =========================
df = pd.read_csv(INPUT_FILE)

# =========================
# FIX YFINANCE MULTIINDEX
# =========================
df.columns = [
    c[0] if isinstance(c, tuple) else c
    for c in df.columns
]

# Elimina columnas repetidas (yfinance bug)
df = df.loc[:, ~df.columns.duplicated()]

# =========================
# DATETIME CLEAN
# =========================
df["Datetime"] = pd.to_datetime(df["Datetime"], utc=True)
df = df.drop_duplicates(subset="Datetime")
df = df.sort_values("Datetime").reset_index(drop=True)

# =========================
# NUMERIC COLUMNS
# =========================
PRICE_COLS = ["Open", "High", "Low", "Close", "Volume"]

for col in PRICE_COLS:
    if col in df.columns:
        df[col] = pd.to_numeric(df[col], errors="coerce")

df = df.dropna(subset=["Open", "High", "Low", "Close"])

# =========================
# INDICATORS
# =========================
df["EMA_20"] = df["Close"].ewm(span=20, adjust=False).mean()
df["EMA_50"] = df["Close"].ewm(span=50, adjust=False).mean()

delta = df["Close"].diff()
gain = delta.clip(lower=0)
loss = -delta.clip(upper=0)

avg_gain = gain.rolling(14).mean()
avg_loss = loss.rolling(14).mean()
rs = avg_gain / avg_loss

df["RSI_14"] = 100 - (100 / (1 + rs))

df["trend"] = np.where(
    df["EMA_20"] > df["EMA_50"], "BULLISH", "BEARISH"
)

# =========================
# FINAL CLEAN
# =========================
df = df.dropna().reset_index(drop=True)

os.makedirs("data", exist_ok=True)
df.to_csv(OUTPUT_FILE, index=False)

print("Indicators fixed and saved correctly")
print(df.tail())
