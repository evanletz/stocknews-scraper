from flask import Blueprint
from flask import render_template, flash, request
from flask_login import current_user
from scraper.models import Article


main = Blueprint('main', __name__)

@main.route('/')
@main.route('/home/')
def home():
    if current_user.is_authenticated:
        page = request.args.get('page', 1, type=int)
        articles = Article.query.filter(Article.ticker_id.in_([t.ticker_id for t in current_user.tickers]))\
            .order_by(Article.article_id.desc()).paginate(page=page, per_page=10)
        if articles.total == 0:
            flash('Add tickers to your watchlist on the Account page \
                to start getting alerts for the latest headlines.', category='warning')
        return render_template('home.html', articles=articles)
    flash('Login to see the latest headlines for your watchlist.', category='warning')
    return render_template('home.html')
