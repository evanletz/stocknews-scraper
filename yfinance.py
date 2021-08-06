import time
from schedule import repeat, every, run_pending
from scraper.yfinance.utils import get_user_tickers, diff_headline, to_article_obj, commit_article, get_all_contacts
from scraper.yfinance.models import Yfinance, Bit, EmailClient


def yf(app):
    with app.app_context():
        print('Starting YF')
        tickers = get_user_tickers()
        print(f'\tTickers: {tickers}')
        yf = Yfinance()
        for ticker in tickers:
            response = yf.request_page(ticker)
            article_info = yf.parse_html(response, ticker)
            if diff_headline(article_info['url'], ticker):
                print(f'\t{article_info['ticker']}: {article_info['title']}')
                article_info['url_shortened'] = Bit().shorten(article_info['url'])
                article_obj = to_article_obj(article_info)
                commit_article(article_obj)
                contacts = get_all_contacts(ticker)
                print(f'\tSending messages to {len(contacts)} users')
                mail = EmailClient()
                for contact in contacts:
                    mail.send_text(contact, article_obj)
                print('\tSent!')
        print('Finished YF')


if __name__ == '__main__':
    pass
