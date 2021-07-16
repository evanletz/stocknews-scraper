import os
import phonenumbers as pn
from flask import Blueprint, current_app
from flask import render_template, flash, redirect, url_for, request
from flask_login import login_user, logout_user, current_user, login_required
from scraper import db, bcrypt, mail
from scraper.models import User, Ticker
from scraper.users.forms import RegistrationForm, LoginForm, UpdateAccountForm, RequestReset, ResetPassword
from scraper.tickers.forms import AddTicker
from scraper.users.utils import save_photo, send_reset_email


users = Blueprint('users', __name__)

@users.route('/register/', methods=['GET','POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('main.home'))
    form = RegistrationForm()
    if form.validate_on_submit():
        pw_hash = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        phone = pn.parse(form.phone.data, 'US').national_number
        user = User(username=form.username.data, email=form.email.data, phone=phone,
                    service=form.service.data, password=pw_hash)
        db.session.add(user)
        db.session.commit()
        flash(f'Account successfully created for {form.username.data}!', category='success')
        return redirect(url_for('users.login'))
    return render_template('register.html', title='Register', form=form)

@users.route('/login/', methods=['GET','POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('main.home'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user, remember=form.remember.data)
            next_page = request.args.get('next')
            return redirect(next_page) if next_page else redirect(url_for('main.home'))
        else:
            flash('Incorrect username and/or password. Try again.', category='danger')
    return render_template('login.html', title='Login', form=form)

@users.route('/logout/')
def logout():
    logout_user()
    flash('You have been successfully logged out!', category='success')
    return redirect(url_for('main.home'))

@users.route('/account/', methods=['GET','POST'])
def account():
    image_file = url_for('static', filename=f'profile_pics/{current_user.image_file}')
    form = AddTicker()
    if 'ticker_id' in request.form.keys():
        ticker = request.form.get('ticker_id')
        to_delete = Ticker.query.filter_by(ticker_id=ticker).first()
        current_user.tickers.pop(current_user.tickers.index(to_delete))
        db.session.commit()
        flash(f'{to_delete.ticker_id} successfully removed from your watchlist!', category='success')
        return redirect(url_for('users.account'))
    elif form.validate_on_submit():
        ticker = Ticker.query.filter_by(ticker_id=form.ticker.data.upper()).first()
        current_user.tickers.append(ticker)
        db.session.commit()
        flash(f'{ticker.ticker_id} successfully added to your watchlist!', category='success')
        return redirect(url_for('users.account'))
    return render_template('account.html', title='Account', image_file=image_file, form=form)

@users.route('/account/update/', methods=['GET','POST'])
@login_required
def update_account():
    form = UpdateAccountForm()
    if form.validate_on_submit():
        if form.photo.data:
            old_photo = os.path.join(current_app.root_path, 'static', 'profile_pics', current_user.image_file)
            new_photo = save_photo(form.photo.data)
            current_user.image_file = new_photo
            os.remove(old_photo)
        current_user.username = form.username.data
        current_user.email = form.email.data
        current_user.phone = form.phone.data
        db.session.commit()
        flash('Your account was successfully updated!', category='success')
        return redirect(url_for('users.update_account'))
    elif request.method == 'GET':
        form.username.data = current_user.username
        form.email.data = current_user.email
        form.phone.data = current_user.phone
        form.photo.data = current_user.image_file
    image_file = url_for('static', filename=f'profile_pics/{current_user.image_file}')
    return render_template('update_account.html', title='Update Account', image_file=image_file, form=form)

@users.route('/account/reset_password/', methods=['GET','POST'])
def request_reset():
    if current_user.is_authenticated:
        return redirect(url_for('main.home'))
    form = RequestReset()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        send_reset_email(user)
        flash('An email has been sent with instructions to reset your password.', category='success')
        redirect(url_for('users.login'))
    return render_template('request_reset.html', title='Reset Password', form=form)

@users.route('/account/reset_password/<token>', methods=['GET','POST'])
def reset_token(token):
    if current_user.is_authenticated:
        return redirect(url_for('main.home'))
    user = User.verify_reset_token(token)
    if not user:
        flash('Invalid or expired token.', category='warning')
        return redirect(url_for('users.request_reset'))
    form = ResetPassword()
    if form.validate_on_submit():
        pw_hash = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user.password = pw_hash
        db.session.commit()
        flash(f'Password successfully updated! You may now log in.', category='success')
        return redirect(url_for('users.login'))
    return render_template('reset_token.html', title='Reset Password', form=form)
