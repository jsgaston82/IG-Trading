import os
import requests

BASE = "https://demo-api.ig.com/gateway/deal"

API_KEY = os.environ["API_KEY"]
USUARIO = os.environ["USUARIO"]
PASSWORD = os.environ["PASSWORD"]

session = requests.Session()
headers = None


def login():
    """
    Login to IG and store session headers (CST + X-SECURITY-TOKEN)
    Works both locally and in GitHub Actions (case-insensitive headers)
    """
    global headers

    response = session.post(
        f"{BASE}/session",
        headers={
            "X-IG-API-KEY": API_KEY,
            "Content-Type": "application/json",
        },
        json={
            "identifier": USUARIO,
            "password": PASSWORD,
        },
    )

    if response.status_code != 200:
        raise Exception(f"IG login failed: {response.text}")

    cst = response.headers.get("CST") or response.headers.get("cst")
    token = (
        response.headers.get("X-SECURITY-TOKEN")
        or response.headers.get("x-security-token")
    )

    if not cst or not token:
        raise Exception(f"Missing IG auth headers: {dict(response.headers)}")

    headers = {
        "X-IG-API-KEY": API_KEY,
        "CST": cst,
        "X-SECURITY-TOKEN": token,
        "Content-Type": "application/json",
    }


def ensure_login():
    if headers is None:
        login()


def get_positions():
    ensure_login()
    r = session.get(f"{BASE}/positions", headers=headers)
    return r.json()


def has_position(epic: str) -> bool:
    positions = get_positions().get("positions", [])
    return any(p["market"]["epic"] == epic for p in positions)


def open_trade(epic: str, direction: str, size: float):
    ensure_login()
    r = session.post(
        f"{BASE}/positions/otc",
        headers=headers,
        json={
            "epic": epic,
            "direction": direction,
            "size": size,
            "orderType": "MARKET",
            "forceOpen": True,
        },
    )
    return r.json()


def close_trade(deal_id: str):
    ensure_login()
    r = session.request(
        "DELETE",
        f"{BASE}/positions/otc",
        headers=headers,
        json={"dealId": deal_id},
    )
    return r.json()

