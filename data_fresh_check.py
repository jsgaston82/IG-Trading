
import json, datetime, os

def signal_is_today(path="signals/signal.json"):
    if not os.path.exists(path):
        return False
    with open(path) as f:
        t = json.load(f).get("time")
    return datetime.datetime.fromisoformat(t).date() == datetime.datetime.utcnow().date()
