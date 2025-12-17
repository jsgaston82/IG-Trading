"""
Descarga datos EURUSD cada 5 minutos usando yfinance
y los guarda de forma incremental en data/eurusd_5m.csv
"""

import os
import pandas as pd
import yfinance as yf
from datetime import datetime, timezone

DATA_DIR = "data"
FILE_PATH = f"{DATA_DIR}/eurusd_5m.csv"
SYMBOL = "EURUSD=X"

os.makedirs(DATA_DIR, exist_ok=True)

def fetch_latest():
    df = yf.download(
        SYMBOL,
        interval="5m",
        period="1d",
        progress=False
    )
    if df.empty:
        return None

    df = df.reset_index()
    df["Datetime"] = df["Datetime"].dt.tz_convert("UTC")
    return df

def append_data(new_df):
    if os.path.exists(FILE_PATH):
        old_df = pd.read_csv(FILE_PATH, parse_dates=["Datetime"])
        combined = pd.concat([old_df, new_df]).drop_duplicates("Datetime")
    else:
        combined = new_df

    combined.sort_values("Datetime", inplace=True)
    combined.to_csv(FILE_PATH, index=False)

if __name__ == "__main__":
    df = fetch_latest()
    if df is not None:
        append_data(df)
        print(f"✅ Datos actualizados: {datetime.now(timezone.utc)}")
    else:
        print("⚠️ No se pudieron descargar datos")
