# main.py
import streamlit as st
from news_fetcher import fetch_guardian_news
from sentiment_analysis import analyze_sentiment
from stock_data import get_stock_data
from correlation_predictor import correlate_and_predict
from recommendation import generate_recommendation
from utils import parse_date_range

st.set_page_config(page_title="Financial Advisor Chatbot")
st.title("🧠 Financial Advisor Chatbot")

# Inputs
keyword = st.text_input("Enter a keyword (e.g., Trump):")
date_range = st.date_input("Select date range:", [])
stock = st.text_input("Enter stock ticker (e.g., AAPL):", "")

if st.button("Fetch and Analyze") and keyword and date_range:
    start_date, end_date = parse_date_range(date_range)

    with st.spinner("Fetching news from Guardian API..."):
        news_df = fetch_guardian_news(keyword, start_date, end_date)
    if news_df.empty:
        st.warning("No news articles found for the given keyword and date range.")
    else:
        st.success(f"Fetched {len(news_df)} articles.")
        st.dataframe(news_df[['webTitle', 'webPublicationDate']])

        with st.spinner("Analyzing sentiment..."):
            sentiment_df = analyze_sentiment(news_df)
        st.success("Sentiment analysis complete.")
        st.dataframe(sentiment_df)

        if stock:
            with st.spinner("Fetching stock data..."):
                stock_df = get_stock_data(stock, start_date, end_date)
            st.line_chart(stock_df['Close'])

            with st.spinner("Analyzing correlation and predicting future prices..."):
                correlation, prediction = correlate_and_predict(sentiment_df, stock_df)
                st.metric("Sentiment-Price Correlation", f"{correlation:.2f}")
                st.metric("Predicted Price (Next Week)", f"${prediction:.2f}")

                suggestion = generate_recommendation(correlation, prediction)
                st.success(f"Investment Recommendation: {suggestion}")
        else:
            st.info("Please enter a stock ticker to continue analysis.")
