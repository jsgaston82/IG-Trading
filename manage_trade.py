from ig_api import get_position, close_trade

pos = get_position()
if not pos:
    exit()

if should_exit(pos):
    close_trade(pos)
