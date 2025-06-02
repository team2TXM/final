# recommendation.py
def generate_recommendation(correlation, predicted_price, current_price=None):
    if current_price is None:
        return "Analyze further"
    delta = predicted_price - current_price
    if correlation > 0.5 and delta > 0:
        return "Buy"
    elif correlation < -0.5 and delta < 0:
        return "Sell"
    else:
        return "Hold"
