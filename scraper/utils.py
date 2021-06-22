import re
import requests
from bs4 import BeautifulSoup
from scraper import db
from scraper.models import Ticker


def get_all_tickers():
    '''
    Get an updated list of all valid stock symbols on the market.
    '''
    result = []
    url = 'https://stockanalysis.com/stocks/'
    response = requests.get(url)

    soup = BeautifulSoup(response.content, 'html.parser')
    links = soup.find_all('a', attrs={'href': re.compile(r'https://stockanalysis.com/stocks/\w')})
    for link in links:
        match = re.search(r'>(.*) - (.*)<', str(link))
        symbol, company_name = match.group(1), match.group(2)
        result.append((symbol, company_name))
    return result

def compare_tickers_table(ticker_list):
    '''
    Given the latest ticker list from online, return old tickers
    to delete and new tickers add to the Ticker table.
    '''
    # The ticker symbol of this list is in the first
    # position of each tuple
    symbol_list = [t[0] for t in ticker_list]

    # The ticker symbol of this list is the ticker_id
    original_symbols = [t.ticker_id for t in Ticker.query.all()]

    symbols_to_delete = list(set(original_symbols) - set(symbol_list))
    symbols_to_add = list(set(symbol_list) - set(original_symbols))
    tickers_to_add = [ticker for ticker in ticker_list if ticker[0] in to_add]
    return symbols_to_delete, tickers_to_add

    
if __name__ == '__main__':
    pass
    
