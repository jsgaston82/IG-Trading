import yfinance as yf
import pandas as pd
import os
from datetime import datetime

os.makedirs("data", exist_ok=True)

FILE = "data/eurusd_5m.csv"

print("Downloading EURUSD 5m data...")

df = yf.download(
    "EURUSD=X",
    interval="5m",
    period="1d",
    progress=False
)

if df.empty:
    print("No data returned from Yahoo")
    exit(0)

df = df.reset_index()

if os.path.exists(FILE):
    old = pd.read_csv(FILE)
    df = pd.concat([old, df], ignore_index=True)
    df = df.drop_duplicates(subset=["Datetime"])

df = df.sort_values("Datetime")

df.to_csv(FILE, index=False)

print("Updated eurusd_5m.csv at", datetime.utcnow())

