import onnxruntime as ort
import numpy as np
import json
import datetime
import joblib

MODEL_PATH = "models/pytorch/eurusd_lstm_daily.onnx"
SCALER_PATH = "models/scalers/eurusd_scaler_daily.pkl"

# cargar scaler
scaler = joblib.load(SCALER_PATH)

# cargar modelo ONNX
session = ort.InferenceSession(MODEL_PATH, providers=["CPUExecutionProvider"])

# nombre de entrada del modelo
input_name = session.get_inputs()[0].name

# features (ejemplo)
X = get_features_6h()          # shape (n_features,)
X = scaler.transform([X])     # shape (1, n_features)
X = np.array(X, dtype=np.float32)

# inferencia
pred = session.run(None, {input_name: X})[0]

direction = "BUY" if pred[0][0] > 0.5 else "SELL"

signal = {
    "time": datetime.datetime.utcnow().isoformat(),
    "direction": direction,
    "confidence": float(pred[0][0])
}

with open("signals/signal.json", "w") as f:
    json.dump(signal, f, indent=2)

print(signal)
