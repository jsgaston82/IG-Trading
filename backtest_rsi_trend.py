import pandas as pd
import json
import os

DATA_FILE = "data/eurusd_5m_indicators.csv"
OUTPUT_FILE = "results/backtest_summary.json"

TP_PIPS = 10
SL_PIPS = 10
PIP_VALUE = 0.0001

df = pd.read_csv(DATA_FILE, parse_dates=["Datetime"])
df = df.sort_values("Datetime").reset_index(drop=True)

trades = []

i = 1
while i < len(df) - 1:
    prev = df.iloc[i - 1]
    cur = df.iloc[i]

    trend = cur["trend"]
    rsi_prev = prev["RSI_14"]
    rsi_now = cur["RSI_14"]
    entry_price = cur["Close"]
    entry_time = cur["Datetime"]

    direction = None

    if trend == "BULLISH" and rsi_prev < 30 and rsi_now >= 30:
        direction = "LONG"
    elif trend == "BEARISH" and rsi_prev > 70 and rsi_now <= 70:
        direction = "SHORT"

    if direction is None:
        i += 1
        continue

    # --- simulate forward ---
    exit_price = entry_price
    result = "SL"
    exit_time = None

    for j in range(i + 1, len(df)):
        high = df.iloc[j]["High"]
        low = df.iloc[j]["Low"]

        if direction == "LONG":
            if high >= entry_price + TP_PIPS * PIP_VALUE:
                exit_price = entry_price + TP_PIPS * PIP_VALUE
                result = "TP"
                exit_time = df.iloc[j]["Datetime"]
                break
            if low <= entry_price - SL_PIPS * PIP_VALUE:
                exit_price = entry_price - SL_PIPS * PIP_VALUE
                exit_time = df.iloc[j]["Datetime"]
                break

        if direction == "SHORT":
            if low <= entry_price - TP_PIPS * PIP_VALUE:
                exit_price = entry_price - TP_PIPS * PIP_VALUE
                result = "TP"
                exit_time = df.iloc[j]["Datetime"]
                break
            if high >= entry_price + SL_PIPS * PIP_VALUE:
                exit_price = entry_price + SL_PIPS * PIP_VALUE
                exit_time = df.iloc[j]["Datetime"]
                break

    pnl_pips = (
        (exit_price - entry_price) / PIP_VALUE
        if direction == "LONG"
        else (entry_price - exit_price) / PIP_VALUE
    )

    trades.append({
        "entry_time": entry_time.isoformat(),
        "exit_time": exit_time.isoformat() if exit_time is not None else None,
        "direction": direction,
        "result": result,
        "pnl_pips": round(pnl_pips, 2)
    })

    i = j + 1

# --- summary ---
total = len(trades)
wins = sum(1 for t in trades if t["result"] == "TP")
losses = sum(1 for t in trades if t["result"] == "SL")
winrate = round(wins / total * 100, 2) if total > 0 else 0
net_pips = round(sum(t["pnl_pips"] for t in trades), 2)

summary = {
    "total_trades": total,
    "wins": wins,
    "losses": losses,
    "winrate_pct": winrate,
    "net_pips": net_pips,
    "tp_pips": TP_PIPS,
    "sl_pips": SL_PIPS
}

os.makedirs("results", exist_ok=True)
with open(OUTPUT_FILE, "w") as f:
    json.dump(summary, f, indent=2)

print("BACKTEST SUMMARY")
print(json.dumps(summary, indent=2))
