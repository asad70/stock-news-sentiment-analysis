'''*****************************************************************************
Purpose: To analyze the news headline of a specific stock.
This program uses Vader SentimentIntensityAnalyzer to calculate the news headline
compound value of a stock for a given day. 
You can analyze multiple stocks at the same time. Ex: 'AAPL, MSFT, F, TSLA' separate
each input by a comma.
You can also analyze all news or a specific date of news.
You can also ignore source: Ex: ignore_source = ['Motley Fool', 'TheStreet.com'] 
Limitations:
This program only analyzes headlines and only for the dates that have available news
on finviz.
-------------------------------------------------------------------
****************************************************************************'''
import pandas as pd
import matplotlib.pyplot as plt
from datetime import date, timedelta
from urllib.request import urlopen, Request
from bs4 import BeautifulSoup
from nltk.sentiment.vader import SentimentIntensityAnalyzer


tickers = input("Enter a valid ticker(for multiple tickers separate by ',') ex 'AAPL, MSFT': ").replace(" ", "")

tickers = tickers.split(",")

# Getting Finviz Data
news_tables = {}        # contains each ticker headlines
for ticker in tickers:
    url = f'https://finviz.com/quote.ashx?t={ticker}'
    req = Request(url=url, headers={'user-agent': 'news'})
    response = urlopen(req)     # taking out html response
            
    html = BeautifulSoup(response, features = 'html.parser')
    news_table = html.find(id = 'news-table') # gets the html object of entire table
    news_tables[ticker] = news_table

ignore_source = ['Motley Fool', 'TheStreet.com'] # sources to exclude
  
# getting date
date_allowed = []
start = input("Enter the date/press enter for today's news (Ex: Dec-27-20) or 'All' for all the available news: ")
if len(start) == 0:
    start = date.today().strftime("%b-%d-%y")   
    date_allowed.append(start)
        
    
# Parsing and Manipulating
parsed = []    
for ticker, news_table in news_tables.items():  # iterating thru key and value
    for row in news_table.findAll('tr'):  # for each row that contains 'tr'
        title = row.a.text
        source = row.span.text
        date = row.td.text.split(' ')
        if len(date) > 1:     # both date and time, ex: Dec-27-20 10:00PM
            date1 = date[0]
            time = date[1]
        else:time = date[0] # only time is given ex: 05:00AM

        if source.strip() not in ignore_source:
            if start.lower() == 'all':
                parsed.append([ticker, date1, time, title])                                
            elif date1 in date_allowed:
                parsed.append([ticker, date1, time, title])                
            else: break
        
        
# Applying Sentiment Analysis
df = pd.DataFrame(parsed, columns=['Ticker', 'date', 'Time', 'Title'])
vader = SentimentIntensityAnalyzer()

# for every title in data set, give the compund score
score = lambda title: vader.polarity_scores(title)['compound']
df['compound'] = df['Title'].apply(score)   # adds compund score to data frame

# Visualization of Sentiment Analysis
df['date'] = pd.to_datetime(df.date).dt.date # takes date comlumn convert it to date/time format

plt.figure(figsize=(6,6))      # figure size
# unstack() allows us to have dates as x-axis
mean_df = df.groupby(['date', 'Ticker']).mean() # avg compund score for each date
mean_df = mean_df.unstack() 

# xs (cross section of compund) get rids of compund label
mean_df = mean_df.xs('compound', axis="columns")
mean_df.plot(kind='bar')
plt.show()
