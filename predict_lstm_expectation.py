import json
import pandas as pd
import numpy as np
import torch
import joblib
from datetime import datetime, timezone

# ===============================
# Paths
# ===============================
DATA_PATH = "data/eurusd_5m_indicators.csv"
MODEL_PATH = "models/pytorch/eurusd_lstm_daily.pth"
SCALER_PATH = "models/scalers/eurusd_scaler_daily.pkl"
CONFIG_PATH = "models/config/eurusd_model_config_daily.json"
OUTPUT_PATH = "results/lstm_expectation.json"

# ===============================
# Load config
# ===============================
with open(CONFIG_PATH) as f:
    config = json.load(f)

SEQ_LEN = config["sequence_length"]

# Usamos EXACTAMENTE las columnas reales
FEATURES = [
    "Open",
    "High",
    "Low",
    "Close",
    "EMA_20",
    "EMA_50",
    "RSI_14"
]

# ===============================
# Load data
# ===============================
df = pd.read_csv(DATA_PATH)

# Seguridad: ordenar y limpiar
df = df.sort_values("Datetime")
df = df.dropna(subset=FEATURES)

# Última ventana temporal
df_window = df.tail(SEQ_LEN)

if len(df_window) < SEQ_LEN:
    raise ValueError("❌ Not enough data for LSTM sequence")

X = df_window[FEATURES].astype(float).values

# ===============================
# Scale
# ===============================
scaler = joblib.load(SCALER_PATH)
X_scaled = scaler.transform(X)

X_tensor = torch.tensor(X_scaled, dtype=torch.float32).unsqueeze(0)

# ===============================
# Load model
# ===============================
model = torch.load(MODEL_PATH, map_location="cpu")
model.eval()

# ===============================
# Predict
# ===============================
with torch.no_grad():
    prediction = model(X_tensor).numpy()[0]

expected_return = float(prediction[0])
confidence = abs(expected_return)

bias = (
    "BULLISH" if expected_return > 0
    else "BEARISH" if expected_return < 0
    else "NEUTRAL"
)

# ===============================
# Output
# ===============================
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
