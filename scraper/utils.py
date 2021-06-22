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

    
if __name__ == '__main__':
    pass
    
