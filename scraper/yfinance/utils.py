from scraper import db
from scraper.models import Ticker, User, Article
from scraper.yfinance.models import Yfinance


def get_user_tickers():
    '''
    Get all tickers currently on every user's watchlist.
    '''
    tickers = set()
    all_users = User.query.all()
    for user in all_users:
        for ticker in user.tickers:
            tickers.add(ticker)
    return tickers

def diff_headline(url, ticker):
    '''
    Compare the given headline with the latest headline
    in the database.
    '''
    db_headline = Article.query.filter_by(ticker_id=ticker.ticker_id).first()
    return db_headline is None or url != db_headline.url

def to_article_obj(info):
    '''
    Concert the given article info into an Article object.
    '''
    article = Article(
        ticker_id=info['ticker'],
        title=info['title'],
        url=info['url'],
        url_shortened=info['url_shortened']
    )
    return article

def commit_article(article):
    '''
    Commit the given Article object to the database.
    '''
    db.session.add(article)
    db.session.commit()

def get_all_contacts(ticker):
    '''
    Get all phone numbers of users watching the given ticker.
    '''
    contacts = [user.phone for user in ticker.users]
    return contacts


if __name__ == '__main__':
    pass