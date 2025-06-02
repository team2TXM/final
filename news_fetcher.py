# news_fetcher.py
import os
import requests
import pandas as pd
from dotenv import load_dotenv

load_dotenv()
GUARDIAN_API_KEY = os.getenv("GUARDIAN_API_KEY")

def fetch_guardian_news(keyword, start_date, end_date):
    url = "https://content.guardianapis.com/search"
    params = {
        "q": keyword,
        "from-date": start_date,
        "to-date": end_date,
        "api-key": GUARDIAN_API_KEY,
        "page-size": 50,
        "show-fields": "bodyText"
    }

    response = requests.get(url, params=params)
    data = response.json()
    if 'response' in data and 'results' in data['response']:
        results = data['response']['results']
        df = pd.DataFrame(results)
        return df
    else:
        return pd.DataFrame()
