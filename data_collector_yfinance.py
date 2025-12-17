import yfinance as yf
import pandas as pd
import os
from datetime import datetime

os.makedirs("data", exist_ok=True)

FILE = "data/eurusd_5m.csv"

# =========================
# DOWNLOAD
# =========================
df = yf.download(
    "EURUSD=X",
    interval="5m",
    period="7d",
    progress=False,
    group_by="column"  # 👈 clave
)

# =========================
# FIX MULTIINDEX
# =========================
if isinstance(df.columns, pd.MultiIndex):
    df.columns = df.columns.get_level_values(0)

df = df.reset_index()

# =========================
# NUMERIC CLEAN
# =========================
PRICE_COLS = ["Open", "High", "Low", "Close", "Volume"]

for col in PRICE_COLS:
    df[col] = pd.to_numeric(df[col], errors="coerce")

df = df.dropna(subset=["Open", "High", "Low", "Close"])

# =========================
# MERGE WITH EXISTING
# =========================
if os.path.exists(FILE):
    old = pd.read_csv(FILE)
    old["Datetime"] = pd.to_datetime(old["Datetime"], utc=True)
    df["Datetime"] = pd.to_datetime(df["Datetime"], utc=True)

    df = pd.concat([old, df], ignore_index=True)
    df = df.drop_duplicates(subset="Datetime")

# =========================
# FINAL
# =========================
df = df.sort_values("Datetime").reset_index(drop=True)
df.to_csv(FILE, index=False)

print("EURUSD 5m data updated:", datetime.utcnow())
