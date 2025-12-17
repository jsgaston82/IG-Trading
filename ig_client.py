
import os
import requests

BASE_URL = os.environ.get("IG_BASE_URL", "https://demo-api.ig.com/gateway/deal")
API_KEY = os.environ.get("API_KEY")
USERNAME = os.environ.get("USUARIO")
PASSWORD = os.environ.get("PASSWORD")

session = requests.Session()
headers = {}

def login():
    global headers
    r = session.post(
        f"{BASE_URL}/session",
        headers={
            "X-IG-API-KEY": API_KEY,
            "Content-Type": "application/json",
            "Accept": "application/json",
        },
        json={"identifier": USERNAME, "password": PASSWORD},
    )
    r.raise_for_status()
    headers = {
        "X-IG-API-KEY": API_KEY,
        "CST": r.headers["CST"],
        "X-SECURITY-TOKEN": r.headers["X-SECURITY-TOKEN"],
        "Content-Type": "application/json",
        "Accept": "application/json",
    }

def get_positions():
    if not headers:
        login()
    return session.get(f"{BASE_URL}/positions", headers=headers).json()

def has_position(epic):
    pos = get_positions()
    return any(p["market"]["epic"] == epic for p in pos.get("positions", []))

def open_trade(epic, direction, size):
    if not headers:
        login()
    payload = {
        "epic": epic,
        "direction": direction,
        "size": size,
        "orderType": "MARKET",
        "forceOpen": True,
    }
    r = session.post(f"{BASE_URL}/positions/otc", headers=headers, json=payload)
    r.raise_for_status()
    return r.json()

def close_trade(deal_id):
    if not headers:
        login()
    r = session.request(
        "DELETE",
        f"{BASE_URL}/positions/otc",
        headers=headers,
        json={"dealId": deal_id},
    )
    r.raise_for_status()
    return r.json()
