import pandas as pd

INPUT_FILE = "data/eurusd_5m.csv"
OUTPUT_FILE = "data/eurusd_5m_indicators.csv"

# --- Load data ---
df = pd.read_csv(INPUT_FILE, parse_dates=["Datetime"])

# --- Sort & remove duplicated timestamps (keep last candle) ---
df = (
    df.sort_values("Datetime")
      .drop_duplicates(subset="Datetime", keep="last")
      .reset_index(drop=True)
)

# --- Indicators ---
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

# --- Save ---
df.to_csv(OUTPUT_FILE, index=False)

print("Indicators updated:", OUTPUT_FILE)
