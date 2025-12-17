import json
from datetime import datetime, timezone

LSTM_PATH = "results/lstm_expectation.json"
TREND_PATH = "results/trend_status.json"
ENTRY_PATH = "results/entry_signal.json"
OUTPUT_PATH = "results/decision.json"

# ========= LOAD FILES =========
with open(LSTM_PATH) as f:
    lstm = json.load(f)

with open(TREND_PATH) as f:
    trend = json.load(f)

with open(ENTRY_PATH) as f:
    entry = json.load(f)

decision = {
    "timestamp": datetime.now(timezone.utc).isoformat(),
    "action": "NO_TRADE",
    "direction": None,
    "reason": []
}

# ========= LOGIC =========
if lstm["confidence"] < 0.2:
    decision["reason"].append("Low LSTM confidence")

elif lstm["bias"] != trend["trend"]:
    decision["reason"].append("Trend mismatch")

elif entry["signal"] == "NONE":
    decision["reason"].append("No entry signal")

else:
    decision["action"] = "OPEN_TRADE"
    decision["direction"] = lstm["bias"]
    decision["reason"].append("All conditions aligned")

# ========= SAVE =========
with open(OUTPUT_PATH, "w") as f:
    json.dump(decision, f, indent=2)

print("✅ Decision evaluated")
print(decision)
