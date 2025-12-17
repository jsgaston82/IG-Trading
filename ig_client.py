import os
import requests

BASE = "https://demo-api.ig.com/gateway/deal"

API_KEY = os.environ["API_KEY"]
USERNAME = os.environ["USUARIO"]
PASSWORD = os.environ["PASSWORD"]

session = requests.Session()
HEADERS = None


def login():
    global HEADERS

    r = session.post(
        f"{BASE}/session",
        headers={
            "X-IG-API-KEY": API_KEY,
            "Content-Type": "application/json",
            "Accept": "application/json",
            "Version": "2",
        },
        json={
            "identifier": USERNAME,
            "password": PASSWORD,
        },
        timeout=10,
    )

    if r.status_code != 200:
        raise Exception(f"IG login failed: {r.status_code} {r.text}")

    # IG sometimes returns lowercase headers
    headers = {k.lower(): v for k, v in r.headers.items()}

    cst = headers.get("cst")
    token = headers.get("x-security-token")

    if not cst or not token:
        raise Exception(f"IG login failed, headers: {headers}")

    HEADERS = {
        "X-IG-API-KEY": API_KEY,
        "CST": cst,
        "X-SECURITY-TOKEN": token,
        "Content-Type": "application/json",
        "Accept": "application/json",
        "Version": "2",
    }


def ensure_login():
    if HEADERS is None:
        login()


def get_positions():
    ensure_login()
    r = session.get(f"{BASE}/positions", headers=HEADERS, timeout=10)
    r.raise_for_status()
    return r.json()


def has_position(epic: str) -> bool:
    data = get_positions()
    for p in data.get("positions", []):
        if p["market"]["epic"] == epic:
            return True
    return False


def open_trade(epic: str, direction: str, size: float):
    ensure_login()
    r = session.post(
        f"{BASE}/positions/otc",
        headers=HEADERS,
        json={
            "epic": epic,
            "direction": direction,
            "size": size,
            "orderType": "MARKET",
            "forceOpen": True,
        },
        timeout=10,
    )
    r.raise_for_status()
    return r.json()


def close_trade(deal_id: str):
    ensure_login()
    r = session.delete(
        f"{BASE}/positions/otc",
        headers=HEADERS,
        json={"dealId": deal_id},
        timeout=10,
    )
    r.raise_for_status()
    return r.json()
