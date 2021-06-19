from datetime import datetime
from flask_login import UserMixin
from scraper import db, login_manager


user_ticker = db.Table(
    'user_ticker',
    db.Column('user_id', db.Integer, db.ForeignKey('user.user_id'), primary_key=True),
    db.Column('ticker_id', db.String, db.ForeignKey('ticker.ticker_id'), primary_key=True)
)

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

class User(db.Model, UserMixin):
    __tablename__ = 'user'
    user_id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(15), unique=True, nullable=False)
    password = db.Column(db.String(60), nullable=False)
    image_file = db.Column(db.String(50), nullable=False, default='default.jpeg')
    first_name = db.Column(db.String(15))
    last_name = db.Column(db.String(25))
    phone = db.Column(db.Integer, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    active = db.Column(db.Boolean, default=True)
    tickers = db.relationship(
        'Ticker', secondary=user_ticker, back_populates='users'
    )

    def __repr__(self):
        return f'User object <{self.user_id}>'

    def get_id(self):
        return self.user_id

class Ticker(db.Model):
    __tablename__ = 'ticker'
    ticker_id = db.Column(db.String, primary_key=True)
    company_name = db.Column(db.String(50))
    active = db.Column(db.Boolean, default=True)
    users = db.relationship(
        'User', secondary=user_ticker, back_populates='tickers'
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
