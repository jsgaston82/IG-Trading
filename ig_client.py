import os
import requests

BASE = "https://demo-api.ig.com/gateway/deal"

API_KEY = os.environ["API_KEY"]
USER = os.environ["USUARIO"]
PASSWORD = os.environ["PASSWORD"]

session = requests.Session()
headers = None

def login():
    global headers

    r = session.post(
        f"{BASE}/session",
        headers={
            "X-IG-API-KEY": API_KEY,
            "Content-Type": "application/json",
            "Accept": "application/json"
        },
        json={
            "identifier": USER,
            "password": PASSWORD
        }
    )

    if r.status_code != 200:
        raise Exception(f"IG login failed: {r.status_code} {r.text}")

    headers = {
        "X-IG-API-KEY": API_KEY,
        "CST": r.headers["CST"],
        "X-SECURITY-TOKEN": r.headers["X-SECURITY-TOKEN"],
        "Content-Type": "application/json",
        "Accept": "application/json"
    }

def ensure_login():
    if headers is None:
        login()

def get_positions():
    ensure_login()
    return session.get(f"{BASE}/positions", headers=headers).json()

def close_trade(deal_id):
    ensure_login()
    return session.request(
        "DELETE",
        f"{BASE}/positions/otc",
        headers=headers,
        json={"dealId": deal_id}
    ).json()
