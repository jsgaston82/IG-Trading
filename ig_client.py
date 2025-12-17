
import os, requests
BASE="https://demo-api.ig.com/gateway/deal"
API_KEY=os.environ["API_KEY"]
U=os.environ["USUARIO"]
P=os.environ["PASSWORD"]
s=requests.Session()
h={}
def login():
    global h
    r=s.post(f"{BASE}/session",headers={"X-IG-API-KEY":API_KEY,"Content-Type":"application/json"},
             json={"identifier":U,"password":P})
    h={"X-IG-API-KEY":API_KEY,"CST":r.headers["CST"],"X-SECURITY-TOKEN":r.headers["X-SECURITY-TOKEN"],
       "Content-Type":"application/json"}
def get_positions():
    if not h: login()
    return s.get(f"{BASE}/positions",headers=h).json()
def has_position(epic):
    return any(p["market"]["epic"]==epic for p in get_positions().get("positions",[]))
def open_trade(epic, direction, size):
    if not h: login()
    return s.post(f"{BASE}/positions/otc",headers=h,
        json={"epic":epic,"direction":direction,"size":size,"orderType":"MARKET","forceOpen":True}).json()
def close_trade(deal):
    if not h: login()
    return s.request("DELETE",f"{BASE}/positions/otc",headers=h,json={"dealId":deal}).json()
