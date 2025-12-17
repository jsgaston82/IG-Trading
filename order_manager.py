
import json, os
from ig_client import open_trade, has_position
from notifier import send
from position_size import compute
from data_fresh_check import signal_is_today

from atr_utils import compute_atr_pips




EPIC = os.environ.get("EPIC", "CS.D.EURUSD.MINI.IP")

if not signal_is_today():
    send("❌ Señal no es de hoy")
    exit()

with open("signals/signal.json") as f:
    sig = json.load(f)

if has_position(EPIC):
    send("ℹ️ Ya existe posición abierta")
    exit()

size = compute(
    balance=float(os.environ.get("ACCOUNT_BALANCE", 10000)),
    risk_pct=float(os.environ.get("RISK_PCT", 0.005)),
    stop_pips = compute_atr_pips()
    tp_pips = stop_pips * 2  # RR 1:2,
)

r = open_trade(EPIC, sig["direction"], size)
send(f"✅ Orden abierta {sig['direction']} size={size}\n{r}")
