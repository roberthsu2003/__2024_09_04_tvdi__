from . import auth
from flask import render_template,request,session,redirect,url_for
from wtforms import EmailField,BooleanField,PasswordField,SubmitField
from wtforms.validators import DataRequired,Length
from flask_wtf import FlaskForm
from datasource import get_password
from werkzeug.security import check_password_hash

class MyForm(FlaskForm):
    email_field = EmailField("Email address",validators=[DataRequired("必需要有資料")])
    password_field = PasswordField("請輸入密碼",validators=[DataRequired("必需要有資料"),Length(5,10)])
    submit_field = SubmitField("確定送出")

@auth.route("/login",methods=['POST','GET'])
def login():
    myForm = MyForm()
    if request.method == "POST" and myForm.validate():
        email = myForm.email_field.data
        password = myForm.password_field.data
        try:
            username, password_hash = get_password(email)
            if check_password_hash(password_hash,password):
                session['username'] = username
                return redirect(url_for('index'))
            else:
                myForm.password_field.errors.append("登入失敗")
        except:
            myForm.password_field.errors.append("登入失敗")
    return render_template('auth/login.j2',myform = myForm)