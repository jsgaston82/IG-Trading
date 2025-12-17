import json
from ig_api import has_position, open_trade

with open("signals/signal.json") as f:
    signal = json.load(f)

if has_position():
    exit()

open_trade(signal["direction"])
