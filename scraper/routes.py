from flask import render_template
from scraper import app


articles = [
    {'ticker_id': 'CHWY',
     'title': 'Test Title 1',
     'url': 'http://testurl1.com/test1'},
    {'ticker_id': 'AAPL',
     'title': 'Test Title 2',
     'url': 'http://testurl2.com/test2'},
    {'ticker_id': 'NIO',
     'title': 'Test Title 3',
     'url': 'http://testurl3.com/test3'}
]

@app.route('/')
@app.route('/home')
def home():
    return render_template('home.html', articles=articles)
