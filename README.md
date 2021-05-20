# stocknews-scraper

## Use Case
Every fixed amount of time (i.e. 10 min), iterate through the given list of stock tickers. Get the latest Yahoo! Finance article for each ticker via web scraping. If the article is new, send the article to interested people via email SMS.

## Triggers
1. Each fixed time interval
2. Latest article is new

## Actors
1. Web scraper
2. Ticker
3. Article 
4. API
5. JSON parser
6. Database
7. Bitly link converter
8. Email

## Preconditions
1. Yahoo! Finance data can be accessed publicly
2. Yahoo! Finance domain is alive and healthy
3. Web scraper has stable internet connection
4. Bitly account has enough free conversion credits

## Goals
1. Successfully send new Yahoo! Finance articles to the proper interested people.

## Process Steps
1. At every fixed time interval, the process begins
2. Web scraper sends GET request to API to get list of tickers and latest article for each and receives JSON response from API
3. Parse JSON response and convert data to list of Ticker objects
4. Iterate through list of ticker objects
5. Web scraper sends GET request to Yahoo! Finance to get latest article and receives response
6. Parse JSON response to get latest article info
7. Compare article link from Yahoo! Finance response to article link from API response
8. If article links are not the same, Web scraper sends PUT request to API using article info
9. Parse JSON response and convert data to Article object
10. Update database with latest article for ticker
11. Create Email object and send GET request for list of contacts associated with ticker and receives response
12. Parse response and convert each contact to a Contact object
13. Convert article link to bitly link
14. Send email SMS with ticker symbol, article title and bitly link to each contact