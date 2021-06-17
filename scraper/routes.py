from flask import render_template, flash, redirect, url_for
from flask_login import login_user, logout_user, current_user
from scraper import app, db, bcrypt
from scraper.models import User, Article
from scraper.forms import RegistrationForm, LoginForm


@app.route('/')
@app.route('/home')
def home():
    return render_template('home.html', articles=Article.query.all())

@app.route('/register', methods=['GET','POST'])
def register():
    if current_user.is_authenticated():
        return redirect(url_for('home'))
    form = RegistrationForm()
    if form.validate_on_submit():
        pw_hash = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user = User(username=form.username.data, email=form.email.data, phone=form.phone.data, password=pw_hash)
        db.session.add(user)
        db.session.commit()
        flash(f'Account successfully created for {form.username.data}!', category='success')
        return redirect(url_for('login'))
    return render_template('register.html', title='Register', form=form)

@app.route('/login', methods=['GET','POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user, remember=form.remember.data)
            return redirect(url_for('home'))
        else:
            flash('Incorrect email and/or password. Try again.', category='danger')
    return render_template('login.html', title='Login', form=form)

@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('home'))
