import time
from schedule import repeat, every, run_pending
from scraper.yfinance.utils import get_user_tickers, diff_headline, to_article_obj, commit_article, get_all_contacts
from scraper.yfinance.models import Yfinance, Bit, EmailClient


@repeat(every(10).minutes)
def main():
    tickers = get_user_tickers()
    print(tickers)
    yf = Yfinance()
    for ticker in tickers:
        response = yf.request_page(ticker)
        article_info = yf.parse_html(response, ticker)
        if diff_headline(article_info['url'], ticker):
            article_info['url_shortened'] = Bit().shorten(article_info['url'])
            article_obj = to_article_obj(article_info)
            commit_article(article_obj)
            contacts = get_all_contacts(ticker)
            mail = EmailClient()
            for contact in contacts:
                mail.send_text(contact, article_obj)


if __name__ == '__main__':
    while True:
        run_pending()
        time.sleep(1)
