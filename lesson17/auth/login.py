from flask import render_template,request,redirect,url_for
from flask_wtf import FlaskForm
from wtforms import EmailField,BooleanField,PasswordField,SubmitField
from wtforms.validators import InputRequired,Length
from werkzeug.security import check_password_hash
from . import auth

class MyForm(FlaskForm):
    email_field = EmailField("Email address",validators=[InputRequired("必需要有資料")])
    password_field = PasswordField("請輸入密碼",validators=[InputRequired("必需要有資料"),Length(5,10)])
    submit_field = SubmitField("確定送出")

@auth.route("/login",methods=['POST','GET'])
def login():
    myForm = MyForm()
    if request.method == "POST" and myForm.validate():
        email = myForm.email_field.data
        password = myForm.password_field.data

        return redirect(url_for('index'))
    return render_template('auth/login.j2',myform = myForm)