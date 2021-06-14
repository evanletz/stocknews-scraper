from flask import render_template
from scraper import app
from scraper.models import Article


@app.route('/')
@app.route('/home')
def home():
    return render_template('home.html', articles=Article.query.all())
