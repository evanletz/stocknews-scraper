import time
from schedule import repeat, every, run_pending
from scraper.tickers.utils import get_all_tickers, compare_tickers_table, update_tickers_table


def ut(app):
    '''
    Each day at 4 AM local, get an updated list of stock tickers via web scraping.
    Update the tickers from the Ticker table in the database as needed.
    '''
    with app.app_context():
        print('Starting UT')
        tickers = get_all_tickers()
        delete, add = compare_tickers_table(tickers)
        print(f'\tDeleting {len(delete)} and adding {len(add)} tickers')
        update_tickers_table(delete, add)
        print('\tSuccess!')
        print('Finished UT')


if __name__ == '__main__':
    pass
