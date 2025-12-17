
def compute(balance, risk_pct, stop_pips, pip_value=10):
    risk = balance * risk_pct
    loss_per_lot = stop_pips * pip_value
    if loss_per_lot <= 0:
        return 0
    return max(1, int(risk / loss_per_lot))
