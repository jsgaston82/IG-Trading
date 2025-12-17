"""
Cálculo de ATR dinámico para EURUSD usando datos 5m
"""

import pandas as pd

PIP_SIZE = 0.0001

def compute_atr_pips(
    csv_path="data/eurusd_5m.csv",
    period=14,
    multiplier=1.5,
):
    df = pd.read_csv(csv_path)

    if len(df) < period + 1:
        raise ValueError("No hay suficientes datos para ATR")

    df["H-L"] = df["High"] - df["Low"]
    df["H-PC"] = abs(df["High"] - df["Close"].shift(1))
    df["L-PC"] = abs(df["Low"] - df["Close"].shift(1))

    df["TR"] = df[["H-L", "H-PC", "L-PC"]].max(axis=1)
    df["ATR"] = df["TR"].rolling(period).mean()

    atr_price = df["ATR"].iloc[-1]
    atr_pips = (atr_price / PIP_SIZE) * multiplier

    return round(atr_pips, 1)
