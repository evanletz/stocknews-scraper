import time
from scraper.tickers.utils import get_content, parse_content, compare_tickers_table, update_tickers_table


def ut(app):
    '''
    Get an updated list of stock tickers via web scraping.
    Update the tickers from the Ticker table in the database as needed.
    '''
    with app.app_context():
        print('Starting UT')
        print('\tRequesting HTML content')
        html = get_content()
        print('\tParsing HTML content')
        tickers = parse_content(html)
        delete, add = compare_tickers_table(tickers)
        print(f'\tDeleting {len(delete)} and adding {len(add)} tickers')
        update_tickers_table(delete, add)
        print('\tSuccess!')
        print('Finished UT')


if __name__ == '__main__':
    pass
