import os
import requests
from datetime import datetime
from dateutil.relativedelta import relativedelta
from pathlib import Path
import pandas as pd
import time
from langdetect import detect

class FinnHub:
    def __init__(self, start_date, end_date, ticker, dir_path):
        self.max_call = 60
        self.time_sleep = 60
        self.nb_request = 0
        self.finnhub_key = "cqbt2f1r01qmbcu8s2mgcqbt2f1r01qmbcu8s2n0"  # Replace with your FinnHub API key
        self.news_header = ['category', 'datetime', 'headline', 'id', 'image', 'related', 'source', 'summary', 'url']
        self.start_date = start_date
        self.end_date = end_date
        self.ticker = ticker
        self.ticker_request = ticker
        self.dir_path = dir_path
        self.df = pd.DataFrame()
        self.start_date_ = datetime.strptime(start_date, "%Y-%m-%d")
        self.end_date_ = datetime.strptime(end_date, "%Y-%m-%d")

    def iterate_day(func):
        def wrapper_(self, *args, **kwargs):
            delta_date_ = (self.end_date_ - self.start_date_).days
            date_ = self.start_date
            date_obj = self.start_date_
            for _ in range(delta_date_ + 1):
                self.nb_request += 1
                func(self, date_)
                date_obj += relativedelta(days=1)
                date_ = date_obj.strftime("%Y-%m-%d")
                if self.nb_request >= self.max_call:
                    time.sleep(self.time_sleep)
                    self.nb_request = 0
        return wrapper_

    @iterate_day
    def req_new(self, date_):
        url = f'https://finnhub.io/api/v1/company-news?symbol={self.ticker_request}&from={date_}&to={date_}&token={self.finnhub_key}'
        response = requests.get(url)
        data = response.json()
        if not data:
            return
        temp_df = pd.DataFrame(data)
        self.df = pd.concat([self.df, temp_df], ignore_index=True)

    def clean_data(self):
        self.df = self.df.dropna(subset=['headline', 'datetime'])
        self.df = self.df[self.df['headline'].str.strip() != '']
        self.df = self.df.drop_duplicates(subset='headline')

    def lang_review(self):
        self.df = self.df[self.df['headline'].apply(lambda x: detect(x)) == 'en']

    def save_to_csv(self):
        file_path = os.path.join(self.dir_path, 'aapl_news_data.csv')
        self.df.to_csv(file_path, index=False)
        print(f"Data saved to {file_path}")

# Example usage
if __name__ == "__main__":
    # Initialize the parameters
    start_date = "2023-07-29"
    end_date = "2024-07-29"
    ticker = 'AAPL'
    dir_path = os.path.dirname(os.path.realpath(__file__)) + '/output/' + start_date + '_' + end_date + "/"
    
    # Create output directory if it doesn't exist
    Path(dir_path).mkdir(parents=True, exist_ok=True)

    # Create an instance of FinnHub
    finnhub = FinnHub(
        start_date=start_date,
        end_date=end_date,
        ticker=ticker,
        dir_path=dir_path
    )

    # Fetch news data
    finnhub.req_new(start_date)
    finnhub.clean_data()
    finnhub.lang_review()
    finnhub.save_to_csv()

