import requests
import os

API_KEY = os.environ["API_KEY"]
USERNAME = os.environ["USUARIO"]
PASSWORD = os.environ["PASSWORD"]

BASE_URL = "https://demo-api.ig.com/gateway/deal"

# 1. Login
headers = {
    "X-IG-API-KEY": API_KEY,
    "Content-Type": "application/json",
    "Accept": "application/json"
}

data = {
    "identifier": USERNAME,
    "password": PASSWORD
}

r = requests.post(f"{BASE_URL}/session", json=data, headers=headers)
tokens = r.headers

CST = tokens["CST"]
SECURITY_TOKEN = tokens["X-SECURITY-TOKEN"]

# 2. Abrir posición
headers.update({
    "CST": CST,
    "X-SECURITY-TOKEN": SECURITY_TOKEN
})

order = {
    "epic": "CS.D.EURUSD.MINI.IP",
    "direction": "BUY",
    "size": 1,
    "orderType": "MARKET",
    "currencyCode": "EUR",
    "forceOpen": True
}

resp = requests.post(f"{BASE_URL}/positions/otc", json=order, headers=headers)
print(resp.json())
