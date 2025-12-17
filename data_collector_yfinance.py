
import yfinance as yf, pandas as pd, os
from datetime import datetime
os.makedirs("data", exist_ok=True)
FILE="data/eurusd_5m.csv"
df = yf.download("EURUSD=X", interval="5m", period="1d", progress=False)
df = df.reset_index()
if os.path.exists(FILE):
    old = pd.read_csv(FILE)
    df = pd.concat([old, df]).drop_duplicates("Datetime")
df.sort_values("Datetime").to_csv(FILE, index=False)
print("Updated", datetime.utcnow())
