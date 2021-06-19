import os
from flask import render_template, flash, redirect, url_for, request
from flask_login import login_user, logout_user, current_user, login_required
import secrets
from PIL import Image
from scraper import app, db, bcrypt
from scraper.models import User, Article
from scraper.forms import RegistrationForm, LoginForm, UpdateAccountForm


@app.route('/')
@app.route('/home')
def home():
    return render_template('home.html', articles=Article.query.all())

@app.route('/register', methods=['GET','POST'])
def register():
    if current_user.is_authenticated:
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
        user = User.query.filter_by(username=form.username.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user, remember=form.remember.data)
            next_page = request.args.get('next')
            return redirect(next_page) if next_page else redirect(url_for('home'))
        else:
            flash('Incorrect username and/or password. Try again.', category='danger')
    return render_template('login.html', title='Login', form=form)

@app.route('/logout')
def logout():
    logout_user()
    flash('You have been successfully logged out!', category='success')
    return redirect(url_for('home'))

@app.route('/account/')
def account():
    image_file = url_for('static', filename=f'profile_pics/{current_user.image_file}')
    return render_template('account.html', title='Account', image_file=image_file)

def save_photo(form_photo):
    random_hex = secrets.token_hex(8)
    _, file_ext = os.path.splitext(form_photo.filename)
    filename = random_hex + file_ext
    filepath = os.path.join(app.root_path, 'static', 'profile_pics', filename)
    output_size = (125, 125)
    img = Image.open(form_photo)
    img.thumbnail(output_size)
    img.save(filepath)
    return filename

@app.route('/account/update/', methods=['GET','POST'])
@login_required
def update_account():
    form = UpdateAccountForm()
    if form.validate_on_submit():
        if form.photo.data:
            old_photo = os.path.join(app.root_path, 'static', 'profile_pics', current_user.image_file)
            new_photo = save_photo(form.photo.data)
            current_user.image_file = new_photo
            os.remove(old_photo)
        current_user.username = form.username.data
        current_user.email = form.email.data
        current_user.phone = form.phone.data
        db.session.commit()
        flash('Your account was successfully updated!', category='success')
        redirect(url_for('update_account'))
    elif request.method == 'GET':
        form.username.data = current_user.username
        form.email.data = current_user.email
        form.phone.data = current_user.phone
        form.photo.data = current_user.image_file
    image_file = url_for('static', filename=f'profile_pics/{current_user.image_file}')
    return render_template('update_account.html', title='Update Account', image_file=image_file, form=form)
