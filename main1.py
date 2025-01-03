import pandas as pd

# Load the datasets
stock_data = pd.read_csv('daily_stock_data1.csv', parse_dates=['Date'])
sentiment_data = pd.read_csv('daily_sentiment_aggregated.csv', parse_dates=['Date'])

# Merge the DataFrames on 'date' column
merged_data = pd.merge(stock_data, sentiment_data, on='Date', how='inner')

# Save the merged DataFrame to a new CSV file
merged_data.to_csv('merged_stock_sentiment_data1.csv', index=False)

print("Merged data saved to 'merged_stock_sentiment_data1.csv'")
