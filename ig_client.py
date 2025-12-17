import os
import requests

BASE = "https://demo-api.ig.com/gateway/deal"

API_KEY = os.environ["API_KEY"]
U = os.environ["USUARIO"]
P = os.environ["PASSWORD"]

s = requests.Session()
HEADERS = {}

def login():
    global HEADERS

    r = s.post(
        f"{BASE}/session",
        headers={
            "X-IG-API-KEY": API_KEY,
            "Content-Type": "application/json"
        },
        json={
            "identifier": U,
            "password": P
        }
    )

    # IG devuelve headers en minúsculas en GitHub Actions
    headers = {k.lower(): v for k, v in r.headers.items()}

    cst = headers.get("cst")
    token = headers.get("x-security-token")

    if not cst or not token:
        raise Exception(f"IG login failed. Headers received: {headers}")

    HEADERS = {
        "X-IG-API-KEY": API_KEY,
        "CST": cst,
        "X-SECURITY-TOKEN": token,
        "Content-Type": "application/json"
    }

def get_positions():
    if not HEADERS:
        login()
    return s.get(f"{BASE}/positions", headers=HEADERS).json()

def has_position(epic):
    return any(
        p["market"]["epic"] == epic
        for p in get_positions().get("positions", [])
    )

def open_trade(epic, direction, size):
    if not HEADERS:
        login()
    return s.post(
        f"{BASE}/positions/otc",
        headers=HEADERS,
        json={
            "epic": epic,
            "direction": direction,
            "size": size,
            "orderType": "MARKET",
            "forceOpen": True
        }
    ).json()

def close_trade(deal_id):
    if not HEADERS:
        login()
    return s.request(
        "DELETE",
        f"{BASE}/positions/otc",
        headers=HEADERS,
        json={"dealId": deal_id}
    ).json()
