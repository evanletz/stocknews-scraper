import re
import os
import requests
from bs4 import BeautifulSoup
from flask_login import current_user
from scraper import db
from scraper.models import Ticker
from dotenv import load_dotenv
load_dotenv()


def get_content():
    '''
    Retrieve the HTML content from each page of the target website until
    we get a bad response status code.
    '''
    page = 1
    headers = {'User-Agent': os.getenv('USER_AGENT')}
    content = []
    while True:
        url = f'https://swingtradebot.com/equities?page={page}'
        res = requests.get(url, headers=headers)
        if res.status_code != 200:
            break
        content.append(res)
        page += 1
    return content

def parse_content(content):
    '''
    Parse each page of HTML content to get a clean list of
    tickers and company names.
    '''
    tickers = []
    for res in content:
        soup = BeautifulSoup(res.content, 'html.parser')
        rows = soup.find_all('a', attrs={'href': re.compile(r'/equities/'), 'class': '', 'title': not ''})
        rows_trunc = rows[::2]
        for row in rows_trunc:
            ticker, name = row.text.strip(), row['title'].strip()
            tickers.append((ticker, name))
    return tickers

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

def get_choices():
    choices = [(t.ticker_id) for t in current_user.tickers]
    choices.insert(0, ('All'))
    return choices
