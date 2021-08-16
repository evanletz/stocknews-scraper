import os
import secrets
from PIL import Image
from flask import current_app, url_for
from flask_mail import Message
from scraper import mail


def save_photo(form_photo):
    '''
    Process the new user profile picture.
    '''
    random_hex = secrets.token_hex(8)
    _, file_ext = os.path.splitext(form_photo.filename)
    filename = random_hex + file_ext
    filepath = os.path.join(current_app.root_path, 'static', 'profile_pics', filename)
    output_size = (125, 125)
    img = Image.open(form_photo)
    img.thumbnail(output_size)
    img.save(filepath)
    return filename

def send_reset_email(user):
    '''
    Construct and send the password reset email to the user.
    '''
    token = user.get_reset_token()
    msg = Message('Password Reset Request',
                  sender=current_app.config['MAIL_USERNAME'],
                  recipients=[user.email])
    msg.body = f'''To reset your password, visit the following link:
{url_for('users.reset_token', token=token, _external=True)}
    
If you did not make this request, please ignore this email.
    '''
    mail.send(msg)
