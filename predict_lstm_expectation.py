
import json
import pandas as pd
import numpy as np
import torch
import joblib
from datetime import datetime, timezone

DATA_PATH = "data/eurusd_5m_indicators.csv"
MODEL_PATH = "models/pytorch/eurusd_lstm_daily.pth"
SCALER_PATH = "models/scalers/eurusd_scaler_daily.pkl"
CONFIG_PATH = "models/config/eurusd_model_config_daily.json"
OUTPUT_PATH = "results/lstm_expectation.json"

with open(CONFIG_PATH) as f:
    config = json.load(f)

SEQ_LEN = config["sequence_length"]
FEATURES = config["features"]

df = pd.read_csv(DATA_PATH)
df = df.sort_values("Datetime").tail(SEQ_LEN)

X = df[FEATURES].astype(float).values
scaler = joblib.load(SCALER_PATH)
X_scaled = scaler.transform(X)

X_tensor = torch.tensor(X_scaled, dtype=torch.float32).unsqueeze(0)

model = torch.load(MODEL_PATH, map_location="cpu")
model.eval()

with torch.no_grad():
    prediction = model(X_tensor).numpy()[0]

expected_return = float(prediction[0])
confidence = abs(expected_return)

bias = "BULLISH" if expected_return > 0 else "BEARISH" if expected_return < 0 else "NEUTRAL"

output = {
    "timestamp": datetime.now(timezone.utc).isoformat(),
    "bias": bias,
    "expected_return_pct": round(expected_return * 100, 3),
    "confidence": round(confidence, 3),
    "valid_hours": 24
}

with open(OUTPUT_PATH, "w") as f:
    json.dump(output, f, indent=2)

print("✅ LSTM expectation generated")
print(output)

