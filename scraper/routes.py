from flask import render_template, flash, redirect, url_for
from scraper import app
from scraper.models import Article
from scraper.forms import RegistrationForm, LoginForm


@app.route('/')
@app.route('/home')
def home():
    return render_template('home.html', articles=Article.query.all())

@app.route('/register', methods=['GET','POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        flash(f'Account successfully created for {form.username.data}!', category='success')
        return redirect(url_for('home'))
    return render_template('register.html', title='Register', form=form)

@app.route('/login', methods=['GET','POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        if form.email.data == 'evanletz@gmail.com' and form.password.data == 'password':
            flash(f'Successfully logged in!', category='success')
            return redirect(url_for('home'))
        else:
            flash('Incorrect username and/or password. Try again.', category='danger')
    return render_template('login.html', title='Login', form=form)
