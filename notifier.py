
import os, requests
def send(msg):
    t=os.environ.get("TELEGRAM_TOKEN")
    c=os.environ.get("TELEGRAM_CHAT_ID")
    if t and c:
        requests.post(f"https://api.telegram.org/bot{t}/sendMessage",data={"chat_id":c,"text":msg})
    else:
        print(msg)
