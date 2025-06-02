# recommendation.py
def generate_recommendation(correlation, predicted_price, avg_impact, current_price=None):
    if current_price is None:
        return "Analyze further"
    delta = predicted_price - current_price
    print(delta)
    if (correlation >= 0.5 and avg_impact >= 0.5) and delta < 0:
        return "Strong Buy"
    if avg_impact >= 0.5 and delta < 0:
        return "Buy"
    if avg_impact < 0.5 and delta > 0:
        return "Sell"
    if (correlation < -0.5 and avg_impact < 0.5) and delta > 0:
        return "Strong Sell"
    else:
        return "Hold"
