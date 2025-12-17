
def compute(balance, risk_pct, stop_pips, pip_value=10):
    return max(1, int((balance * risk_pct) / (stop_pips * pip_value)))
