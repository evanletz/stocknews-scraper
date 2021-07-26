import os
import requests
import datetime
from bs4 import BeautifulSoup
import bitlyshortener
from dotenv import load_dotenv
from flask import current_app
from flask_mail import Message
from scraper import mail
load_dotenv()


class Yfinance:

    article_base_url = r'https://finance.yahoo.com'
    article_class = 'js-content-viewer wafer-caas Fw(b) Fz(18px) Lh(23px) LineClamp(2,46px) Fz(17px)--sm1024 Lh(19px)--sm1024 LineClamp(2,38px)--sm1024 mega-item-header-link Td(n) C(#0078ff):h C(#000) LineClamp(2,46px) LineClamp(2,38px)--sm1024 not-isInStreamVideoEnabled'

    def request_page(self, ticker_obj):
        url = fr'{self.article_base_url}/quote/{ticker_obj.ticker_id}/?p={ticker_obj.ticker_id}'
        res = requests.get(url)
        res.raise_for_status()
        return res

    def parse_html(self, res, ticker_obj):
        soup = BeautifulSoup(res.content, 'html.parser')
        article = soup.find_all('a', {'class': self.article_class})[0]
        title = article.contents[2]
        link = self.article_base_url + article.attrs['href']
        info = {'ticker': ticker_obj.ticker_id,
                'company': ticker_obj.company_name,
                'title': title, 
                'url': link}
        return info

class EmailClient:

    @staticmethod
    def _format_msg_len(msg):
        rem_chars = 160 - len(msg)
        result = msg + ' '*rem_chars
        assert len(result) == 160
        return result

    @staticmethod
    def _format_msg_enc(msg):
        msg = msg.replace('\u2019', "'")
        return msg

    def send_text(self, to, article):
        ticker, title, url = article.ticker_id, article.title, article.url_shortened
        body = f"({ticker}) {title} - <{url}>"
        if len(body) < 160:
            body = self._format_msg_len(body)
        body = self._format_msg_enc(body)
        msg = Message(None,
                      sender=current_app.config['MAIL_USERNAME'],
                      recipients=[to])
        msg.body = body
        mail.send(msg)

class Bit:

    def __init__(self):
        token = [os.getenv('BITLY')]
        self.shortener = bitlyshortener.Shortener(tokens=token)

    def shorten(self, url):
        result = self.shortener.shorten_urls([url])
        return result[0]
