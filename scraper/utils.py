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
    tickers_to_add = [ticker for ticker in ticker_list if ticker[0] in symbols_to_add]
    return symbols_to_delete, tickers_to_add

def update_tickers_table(to_delete, to_add):
    '''
    Delete old tickers and add new tickers to the Ticker table.
    '''
    for delete_ticker in to_delete:
        Ticker.query.filter_by(ticker_id=delete_ticker).delete()
    for add_ticker in to_add:
        symbol = add_ticker[0]
        company_name = add_ticker[1]
        ticker = Ticker(ticker_id=symbol, company_name=company_name)
        db.session.add(ticker)
    db.session.commit()

    
if __name__ == '__main__':
    pass
    
