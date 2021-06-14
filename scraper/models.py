from datetime import datetime
from scraper import db


contact_ticker = db.Table(
    'contact_ticker',
    db.Column('contact_id', db.Integer, db.ForeignKey('contact.contact_id'), primary_key=True),
    db.Column('ticker_id', db.String, db.ForeignKey('ticker.ticker_id'), primary_key=True)
)

class Contact(db.Model):
    __tablename__ = 'contact'
    contact_id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String)
    last_name = db.Column(db.String)
    phone = db.Column(db.Integer, nullable=False)
    email = db.Column(db.String)
    active = db.Column(db.Boolean)
    tickers = db.relationship(
        'Ticker', secondary=contact_ticker, back_populates='contacts'
    )

    def __repr__(self):
        return f'Contact object <{self.contact_id}>'

class Ticker(db.Model):
    __tablename__ = 'ticker'
    ticker_id = db.Column(db.String, primary_key=True)
    company_name = db.Column(db.String)
    active = db.Column(db.Boolean, default=True)
    contacts = db.relationship(
        'Contact', secondary=contact_ticker, back_populates='tickers'
    )
    articles = db.relationship('Article', backref=db.backref('ticker'))


    def __repr__(self):
        return f'Ticker object <{self.ticker_id}>'

class Article(db.Model):
    __tablename__ = 'article'
    article_id = db.Column(db.Integer, primary_key=True)
    ticker_id = db.Column(db.String, db.ForeignKey('ticker.ticker_id'))
    title = db.Column(db.String)
    url = db.Column(db.String)
    datetime_found = db.Column(db.DateTime, default=datetime.now())

    def __repr__(self):
        return f'Article object <{self.article_id}>'
