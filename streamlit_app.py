import streamlit as st
from datetime import datetime
from dotenv import load_dotenv
import os

from news_fetcher import fetch_guardian_news
from sentiment_analysis import analyze_sentiment
from stock_data import get_stock_data, get_current_price
from correlation_predictor import correlate_and_predict
from recommendation import generate_recommendation
from utils import parse_chat_input
from gemini_chat import chat_with_gemini  # new

load_dotenv()

st.set_page_config(page_title="💬 Financial Advisor Chatbot")
st.title("🧠 Financial Advisor Chatbot")

# Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = [
        {"role": "assistant", "content": "Hi! I'm your financial advisor. Ask me about U.S. politics news and stocks. For example:\n\n*'Analyze Trump news from 2018-2020 and its impact on AAPL'*"}
    ]

# Display chat history
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# User input via chat
if prompt := st.chat_input("Ask me about political news and stocks..."):
    st.chat_message("user").markdown(prompt)
    st.session_state.messages.append({"role": "user", "content": prompt})

    with st.chat_message("assistant"):
        with st.spinner("Let me look that up..."):
            parsed = parse_chat_input(prompt)  # returns dict with keyword, start_date, end_date, stock, is_structured

            if parsed.get("is_structured"):  # proceed with your existing pipeline
                keyword = parsed["keyword"]
                start_date = parsed["start_date"]
                end_date = parsed["end_date"]
                stock = parsed["stock"]

                # 1. Fetch Guardian news
                news_df = fetch_guardian_news(keyword, start_date, end_date)
                if news_df.empty:
                    response = f"No news found for '{keyword}' between {start_date} and {end_date}."
                else:
                    # 2. Sentiment analysis
                    sentiment_df = analyze_sentiment(news_df)

                    # 3. Get stock data if specified
                    if stock:
                        stock_df = get_stock_data(stock, start_date, end_date)
                        correlation, prediction = correlate_and_predict(sentiment_df, stock_df)
                        current_price = get_current_price(stock)
                        suggestion = generate_recommendation(correlation, prediction, current_price)

                        response = (
                            f"✅ Found {len(news_df)} news articles about **{keyword}**.\n\n"
                            f"📊 Correlation between sentiment and **{stock.upper()}** price: `{correlation:.2f}`\n"
                            f"💡 Predicted price next week: `${prediction:.2f}`\n"
                            f"📈 Recommendation: **{suggestion}**"
                        )
                    else:
                        response = (
                            f"✅ Found {len(news_df)} news articles about **{keyword}**.\n\n"
                            f"You didn’t mention a stock ticker. Try asking something like:\n"
                            f"`How did Trump news from 2018-2020 affect AAPL?`"
                        )
            else:
                # fallback to Gemini if input isn't structured enough
                response = chat_with_gemini(prompt)

        st.markdown(response)
        st.session_state.messages.append({"role": "assistant", "content": response})
