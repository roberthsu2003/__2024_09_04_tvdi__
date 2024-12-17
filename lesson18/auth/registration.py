from . import auth
from flask import render_template
from flask_wtf import FlaskForm
from wtforms import StringField,PasswordField,EmailField

class RegistrationForm(FlaskForm):
    username = StringField('username')
    email = EmailField('Email Address')
    password = PasswordField('New Password')
    confirm =PasswordField('Repeat Password')

@auth.route('/regist')
def regist():
    form = RegistrationForm()
    return render_template('auth/registration.j2',form=form)