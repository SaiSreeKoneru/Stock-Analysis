import pandas as pd
import numpy as np
import holidays
from datetime import datetime  
# Load your news sentiment data
news_sentiment_df = pd.read_csv('aapl_formatted.csv')

# Convert 'datetime' column to datetime format
news_sentiment_df['datetime'] = pd.to_datetime(news_sentiment_df['datetime'])  # If 'datetime' is in UNIX timestamp

# Extract the date part only
news_sentiment_df['date'] = news_sentiment_df['datetime'].dt.date
news_sentiment_df = news_sentiment_df[~news_sentiment_df['datetime'].dt.weekday.isin([5, 6])]
us_holidays = holidays.US(years=[2023, 2024], observed=True)
start_date=datetime(2023,7,29).date()
end_date=datetime(2024,7,29).date()
# Filter holidays that fall within the given date range
holiday_dates = [date for date in us_holidays if start_date <= date <= end_date]
# Group by the 'date' column and compute the average compound score for each day
daily_sentiment_df = news_sentiment_df.groupby('date').agg({
    'compound': 'mean'
}).reset_index()

# Rename columns for clarity
daily_sentiment_df.columns = ['Date', 'Average_Compound']
daily_sentiment_df = daily_sentiment_df.iloc[::-1].reset_index(drop=True)

# Save the aggregated data to a CSV file
daily_sentiment_df.to_csv('daily_sentiment_aggregated.csv', index=False)

print("Data saved to daily_sentiment_aggregated.csv")



print(daily_sentiment_df.head())
