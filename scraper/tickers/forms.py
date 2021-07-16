from flask_wtf import FlaskForm
from flask_login import current_user
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired, Length, ValidationError
from scraper.models import Ticker


class AddTicker(FlaskForm):

    ticker = StringField('Ticker', validators=[DataRequired(), Length(min=1, max=5)])
    submit = SubmitField('Add')

    def validate_ticker(self, ticker):
        db_ticker = Ticker.query.filter_by(ticker_id=ticker.data.upper()).first()
        if db_ticker is None:
            raise ValidationError('Ticker is invalid or cannot be found. Please choose a different one.')
        elif db_ticker in current_user.tickers:
            raise ValidationError('Ticker is already in your watchlist. Please choose a different one.')
