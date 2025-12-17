import yfinance as yf
import pandas as pd
import datetime, os

now = datetime.datetime.utcnow()
if now.weekday() == 5:
    os.remove("data/eurusd_5m.csv")
    exit()

df = yf.download("EURUSD=X", interval="5m", period="1d")
df.to_csv("data/eurusd_5m.csv", mode="a", header=not os.path.exists("data/eurusd_5m.csv"))
