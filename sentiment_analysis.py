# sentiment_analysis.py
from transformers import pipeline, BertTokenizer, BertForSequenceClassification
import pandas as pd

tokenizer = BertTokenizer.from_pretrained("ProsusAI/finbert")
model = BertForSequenceClassification.from_pretrained("ProsusAI/finbert")
classifier = pipeline("sentiment-analysis", model=model, tokenizer=tokenizer)

def analyze_sentiment(news_df):
    sentiments = []
    for text in news_df['fields'].apply(lambda x: x.get('bodyText', '')[:512]):
        result = classifier(text)[0]
        sentiments.append(result)
    result_df = pd.DataFrame(sentiments)
    return pd.concat([news_df, result_df], axis=1)
