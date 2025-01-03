import pandas as pd
import nltk
from nltk.sentiment.vader import SentimentIntensityAnalyzer as sia
from statistics import mean
import ssl

try:
    _create_unverified_https_context = ssl._create_unverified_context
except AttributeError:
    pass
else:
    ssl._create_default_https_context = _create_unverified_https_context

nltk.download('vader_lexicon')

class VaderAnalysis():
    def __init__(self, hist_price, start_date, end_date, ticker, dir_path, sentiment_name, news_header):
        self.start_date = pd.to_datetime(start_date)
        self.end_date = pd.to_datetime(end_date)
        self.ticker = ticker
        self.dir_path = dir_path
        self.news_header = news_header
        self.pd_data = hist_price
        self.sentiment_name = sentiment_name
        self.min_sample = 30
        self.start_debut_tempo = None
        self.end_date_tempo = None

    def check_size(self, date_, delta_day):
        date_ = pd.to_datetime(date_)
        self.start_debut_tempo = date_.timestamp()
        self.end_date_tempo = self.start_debut_tempo + (24 * 60 * 60 * delta_day)
        
        sample_size = len(self.pd_data[
            (self.pd_data[self.news_header[1]] >= self.start_debut_tempo) &
            (self.pd_data[self.news_header[1]] < self.end_date_tempo)
        ])
        
        return sample_size >= self.min_sample

    def vader_analysis(self):
        sia_analyzer = sia()
        results = []
        self.pd_data[self.news_header[1]]=pd.to_datetime(self.pd_data[self.news_header[1]])

        for index in range(len(self.pd_data) - 1):
            current_date = self.pd_data.iloc[index, 0]
            next_date = self.pd_data.iloc[index + 1, 0]
            delta_day = (next_date - current_date).days
            
            if self.check_size(current_date, delta_day):
                # Extract news within the date range
                subset = self.pd_data[
                    (self.pd_data[self.news_header[1]] >= pd.to_datetime(current_date).timestamp()) &
                    (self.pd_data[self.news_header[1]] < pd.to_datetime(next_date).timestamp())
                ]
                
                # Calculate sentiment scores
                scores = []
                for text in subset[self.news_header[2]]:
                    scores.append(sia_analyzer.polarity_scores(text)['compound'])
                
                # Average sentiment score
                avg_sentiment = mean(scores) if scores else 0
                results.append(avg_sentiment)
            else:
                results.append(None)
        
        # Adding results to DataFrame
        self.pd_data[self.sentiment_name] = pd.Series(results + [None] * (len(self.pd_data) - len(results)))

        # Save to CSV
        output_file = f"{self.dir_path}aapl_news_data_with_sentiments.csv"
        self.pd_data.to_csv(output_file, index=False)
        print(f"Sentiment analysis complete. Results saved to {output_file}")

# Example usage
if __name__ == "__main__":
    # Load CSV data
    input_file = 'output\\2023-07-29_2024-07-29\\aapl_news_data.csv'
    hist_price = pd.read_csv(input_file)
    
    # Initialize VaderAnalysis
    va = VaderAnalysis(
        hist_price=hist_price,
        start_date='2023-07-29',
        end_date='2024-07-29',
        ticker='AAPL',
        dir_path='./',
        sentiment_name='Sentiment',
        news_header=['Date', 'Timestamp', 'Headline']  # Adjust based on your CSV column names
    )
    
    # Perform Vader Analysis
    va.vader_analysis()
