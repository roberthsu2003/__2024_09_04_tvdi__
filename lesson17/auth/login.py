from flask import render_template,request,redirect,url_for,session
from flask_wtf import FlaskForm
from wtforms import EmailField,BooleanField,PasswordField,SubmitField
from wtforms.validators import InputRequired,Length
from werkzeug.security import check_password_hash
from . import auth
from datasource import get_password

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
        #沒有該email帳號,會raise錯誤
        try:        
            username ,password_hash = get_password(email)
            if not check_password_hash(password_hash, password):
               myForm.password_field.errors.append('密碼有問題')
            else:
                session['username'] = username
                return redirect(url_for('index'))

        except:
            myForm.password_field.errors.append('帳號有問題')        
        
        
    return render_template('auth/login.j2',myform = myForm)