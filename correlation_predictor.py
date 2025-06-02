import pandas as pd
import numpy as np
from sklearn.linear_model import LinearRegression

def correlate_and_predict(sentiment_df, stock_df):
    # Flatten MultiIndex columns in stock_df
    stock_df.columns = [
        '_'.join(filter(None, col)).strip() if isinstance(col, tuple) else col
        for col in stock_df.columns.values
    ]

    # Fix dates in sentiment_df and stock_df
    sentiment_df['date'] = pd.to_datetime(sentiment_df['webPublicationDate']).dt.date
    sentiment_summary = (
        sentiment_df
        .groupby('date')['label']
        .apply(lambda x: (x.str.upper() == 'POSITIVE').sum())
        .reset_index(name='positive_sentiment')
    )

    stock_df = stock_df.reset_index()  # reset index in case 'Date' is index
    stock_df['date'] = pd.to_datetime(stock_df['Date']).dt.date  # assuming stock_df has 'Date' column after flatten

    # Pick the correct 'Close' column (e.g. 'Close_AAPL')
    close_cols = [col for col in stock_df.columns if col.startswith('Close')]
    if not close_cols:
        raise ValueError("No 'Close' column found in stock_df after flattening columns.")
    close_col = close_cols[0]  # take first one if multiple

    stock_prices = stock_df[['date', close_col]].rename(columns={close_col: 'Close'})

    # Merge on 'date' (outer join to keep all data)
    merged_df = sentiment_summary.merge(stock_prices, on='date', how='outer').sort_values('date')

    # Fill missing values to avoid issues
    merged_df['positive_sentiment'] = merged_df['positive_sentiment'].fillna(0)
    merged_df['Close'] = merged_df['Close'].fillna(method='ffill')

    if len(merged_df) < 2:
        current_price = stock_df['Close_AAPL'].iloc[-1]
        return 0.0, current_price

    correlation = merged_df['positive_sentiment'].corr(merged_df['Close'])

    from sklearn.linear_model import LinearRegression
    X = merged_df[['positive_sentiment']]
    y = merged_df['Close']
    model = LinearRegression().fit(X, y)
    predicted_price = model.predict([[X.iloc[-1].values[0] + 1]])[0]

    return correlation, predicted_price

