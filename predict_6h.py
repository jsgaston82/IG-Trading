import json, joblib, datetime

model = joblib.load("models/eurusd_6h_model.pkl")

X = get_features_6h()  # tu lógica
pred = model.predict(X)[0]

signal = {
    "time": datetime.datetime.utcnow().isoformat(),
    "direction": "BUY" if pred == 1 else "SELL"
}

with open("signals/signal.json", "w") as f:
    json.dump(signal, f)
