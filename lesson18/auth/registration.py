from . import auth
from flask import render_template
from flask_wtf import FlaskForm
from wtforms import StringField,PasswordField,EmailField

class RegistrationForm(FlaskForm):
    username = StringField('使用者名稱')
    email = EmailField('電子郵件')
    password = PasswordField('密碼')
    confirm =PasswordField('再次確認密碼')

@auth.route('/regist')
def regist():
    form = RegistrationForm()
    return render_template('auth/registration.j2',form=form)