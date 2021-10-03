# stock-news-sentiment-analysis


Purpose: To analyze the news headline of a specific stock.
This program uses Vader SentimentIntensityAnalyzer to calculate the news headline compound value of a stock for a given day. 

# How to run:

    python3 'Stock news.py'
    
Analyze multiple stocks at the same time. Ex: 'AAPL, MSFT, F, TSLA' separate each input by a comma.

Analyze all news or a specific date of news. 
Ex: "Enter the date/press enter for today's news (Ex: Dec-27-20) or 'All' for all the available news: " 
hit enter for today's news, enter a specific date, or type all for all the news (limited).

You can also ignore source: Ex: ignore_source = ['Motley Fool', 'TheStreet.com'] 

Limitations:
This program only analyzes headlines and only for the dates that have news available on finviz. 

Example output:
![](sampleoutput.png)



## License

This project is licensed under the MIT License - see the [LICENSE.md](LICENSE.md) file for details.
