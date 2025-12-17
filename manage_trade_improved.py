
from ig_client import get_positions, close_trade
from notifier import send

positions = get_positions()

for p in positions.get("positions", []):
    deal = p.get("dealId")
    pnl = p.get("profitAndLoss", 0)
    if pnl < -50:
        close_trade(deal)
        send(f"🔴 Orden cerrada por pérdida {deal}")
