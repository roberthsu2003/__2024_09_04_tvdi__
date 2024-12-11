from flask import render_template
from flask_wtf import FlaskForm
from wtforms import EmailField,BooleanField,PasswordField,SubmitField
from wtforms.validators import DataRequired,Length
from . import auth

class MyForm(FlaskForm):
    email_field = EmailField("Email address",validators=[DataRequired("必需要有資料")])
    password_field = PasswordField("請輸入密碼",validators=[DataRequired("必需要有資料"),Length(5,10)])
    epaper_field = BooleanField("訂閱電子報")
    submit_field = SubmitField("確定送出")

@auth.route("/login",methods=['POST','GET'])
def login():
    myForm = MyForm()
    return render_template('auth/login.j2',myform = myForm)