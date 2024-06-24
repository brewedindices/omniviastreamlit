import pandas as pd
import random

def van_westendorp_analysis(price_points, responses):
    """Performs Van Westendorp price sensitivity analysis."""
    too_expensive = []
    too_cheap = []
    just_right = []
    too_expensive_data = []
    too_cheap_data = []
    just_right_data = []
    for response in responses:
        for i, price in enumerate(price_points):
            if response == "Too expensive":
                too_expensive_data.append(price)
                too_expensive.append(i)
            elif response == "Too cheap":
                too_cheap_data.append(price)
                too_cheap.append(i)
            elif response == "Just right":
                just_right_data.append(price)
                just_right.append(i)

    # Calculate Optimal Price Range
    too_expensive_avg = sum(too_expensive_data) / len(too_expensive_data) if too_expensive_data else 0
    too_cheap_avg = sum(too_cheap_data) / len(too_cheap_data) if too_cheap_data else 0
    just_right_avg = sum(just_right_data) / len(just_right_data) if just_right_data else 0

    optimal_price_range = (too_cheap_avg, too_expensive_avg)
    return optimal_price_range, too_expensive, too_cheap, just_right

def gabor_granger_analysis(price_points, responses):
    """Performs Gabor-Granger price sensitivity analysis."""
    demand_at_price = {}
    for i, price in enumerate(price_points):
        demand_at_price[price] = responses.count(i)
    return demand_at_price

def analyze_sentiment(responses):
    """Performs sentiment analysis on survey responses."""
    sentiments = []
    for response in responses:
        if isinstance(response, str):
            prompt = f"""Analyze the sentiment of the following text:
            "{response}"
            Provide the sentiment as "positive", "negative", or "neutral".
            """
            sentiment = llm(prompt)
            sentiments.append({"Response": response, "Sentiment": sentiment})
    return sentiments