import time
from schedule import repeat, every, run_pending
from scraper.utils import get_all_tickers, compare_tickers_table, update_tickers_table


@repeat(every().day.at('04:00:00'))
def main():
    '''
    Each day at 4 AM local, get an updated list of stock tickers via web scraping.
    Update the tickers from the Ticker table in the database as needed.
    '''
    tickers = get_all_tickers()
    delete, add = compare_tickers_table(tickers)
    update_tickers_table(delete, add)


if __name__ == '__main__':
    while True:
        run_pending()
        time.sleep(1)
