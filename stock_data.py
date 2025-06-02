# stock_data.py
import yfinance as yf

def get_stock_data(ticker, start_date, end_date):
    df = yf.download(ticker, start=start_date, end=end_date)
    return df

def get_current_price(ticker):
    ticker_obj = yf.Ticker(ticker)
    todays_price = ticker_obj.history(period="1d")['Close']
    if not todays_price.empty:
        return todays_price.iloc[-1]
    else:
        return None  # fallback if no data