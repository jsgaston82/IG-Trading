
from ig_client import get_positions, close_trade
from atr_utils import compute_atr_pips
from notifier import send
atr=compute_atr_pips(multiplier=1.0)
for p in get_positions().get("positions",[]):
    if p.get("profitAndLoss",0)< -atr*10:
        close_trade(p["dealId"])
        send("CLOSE by ATR")
