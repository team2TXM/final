import pandas as pd
import numpy as np

def news_impact(sentiment_df: pd.DataFrame) -> pd.DataFrame:
    """
    Compute an impact score for each news article based on sentiment.

    Args:
        sentiment_df (pd.DataFrame): DataFrame containing at least a 'score' sentiment score
                                     and ideally other relevant columns like 'webTitle'.

    Returns:
        pd.DataFrame: The same DataFrame with a new 'impact_score' column added.
    """

    # Example simple impact score: absolute value of score sentiment times a scaling factor
    # You can customize this formula as needed
    sentiment_df = sentiment_df.copy()
    
    # Make sure 'score' exists
    if 'score' not in sentiment_df.columns:
        raise ValueError("Input DataFrame must contain a 'score' column with sentiment scores.")

    # Impact score as absolute sentiment magnitude, normalized 0 to 1
    max_abs = sentiment_df['score'].abs().max()
    if max_abs == 0:
        sentiment_df['impact_score'] = 0.0
    else:
        sentiment_df['impact_score'] = sentiment_df['score'].abs() / max_abs

    return sentiment_df
