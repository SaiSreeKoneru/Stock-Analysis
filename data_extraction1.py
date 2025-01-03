import pandas as pd
import yfinance as yf
from datetime import datetime

class InitAV:
    def __init__(self):
        self.output_size = 'full'

class HistoricalReturn(InitAV):
    def __init__(self, start_date, end_date, start_date_, end_date_, ticker, daily_return):
        super().__init__()
        self.adj_close = 'Adjusted Close'
        self.daily_open='Open'
        self.day_high='High'
        self.day_low='Low'
        self.daily_volume='Volume'
        self.daily_return = daily_return
        self.start_date = start_date
        self.end_date = end_date
        self.ticker = ticker
        self.pd_data = pd.DataFrame()
        self.start_date_ = start_date_
        self.end_date_ = end_date_
        self.pd_data = None
        
    def historical_price(self):
        # Fetch data from Yahoo Finance
        self.pd_data = yf.download(self.ticker, start=self.start_date, end=self.end_date)
        self.pd_data.index = pd.to_datetime(self.pd_data.index)

        # Drop any rows with missing values
        self.pd_data = self.pd_data.dropna()

        # Select the adjusted close prices within the date range
        self.pd_data = self.pd_data.loc[(self.pd_data.index >= self.start_date) & (self.pd_data.index <= self.end_date)]
        self.pd_data = self.pd_data[['Open','High','Low','Adj Close','Volume']]
        self.pd_data.columns = [self.daily_open,self.day_high,self.day_low,self.adj_close,self.daily_volume]

        # Reverse the DataFrame to ensure chronological order
        self.pd_data = self.pd_data[::-1]

        # Calculate daily returns
        self.pd_data[self.daily_return] = self.pd_data[self.adj_close].pct_change()

        # Reset the index
        self.pd_data = self.pd_data.reset_index(inplace=False)
        return self.pd_data

# Example usage:
if __name__ == "__main__":
    start_date = '2023-08-03'
    end_date = '2024-07-29'
    start_date_ = '2023-08-03'
    end_date_ = '2024-07-29'
    ticker = 'AAPL'
    daily_return = 'Daily Return'
    
    hist_return = HistoricalReturn(start_date, end_date, start_date_, end_date_, ticker, daily_return)
    data = hist_return.historical_price()
    print(data)
    data.to_csv('daily_stock_data1.csv', index=False)
