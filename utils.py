# utils.py
def parse_date_range(date_range):
    if len(date_range) == 2:
        return str(date_range[0]), str(date_range[1])
    return None, None

# utils.py
import re
from datetime import datetime

def parse_chat_input(prompt):
    keyword = None
    start_date = None
    end_date = None
    stock = None

    # Extract date range (e.g. 2018-2020)
    date_match = re.search(r"(\d{4})\s*[-to]+\s*(\d{4})", prompt)
    if date_match:
        start_year, end_year = date_match.groups()
        start_date = f"{start_year}-01-01"
        end_date = f"{end_year}-12-31"

    # Extract stock ticker (e.g. AAPL)
    stock_match = re.search(r"\b[A-Z]{3,5}\b", prompt)
    if stock_match:
        stock = stock_match.group(0)

    # Extract keyword (everything before "news" or just first noun-like word)
    keyword_match = re.search(r"(about|analyze|on|regarding)?\s*([A-Za-z]+)\s+(news|from)", prompt)
    if keyword_match:
        keyword = keyword_match.group(2)

    return {
        "keyword": keyword,
        "start_date": start_date,
        "end_date": end_date,
        "stock": stock
    }
