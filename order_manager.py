
import json, os
from ig_client import open_trade, has_position
from atr_utils import compute_atr_pips
from position_size import compute
from notifier import send
EPIC=os.environ.get("EPIC","CS.D.EURUSD.MINI.IP")
with open("signals/signal.json") as f:
    sig=json.load(f)
if has_position(EPIC): exit()
stop=compute_atr_pips()
size=compute(float(os.environ["ACCOUNT_BALANCE"]),float(os.environ["RISK_PCT"]),stop)
r=open_trade(EPIC,sig["direction"],size)
send(f"OPEN {sig['direction']} size={size} SL={stop}pips\n{r}")
