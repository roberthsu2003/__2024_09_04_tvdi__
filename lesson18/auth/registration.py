from . import auth
from flask import render_template,request,redirect,url_for
from flask_wtf import FlaskForm
from wtforms import StringField,PasswordField,EmailField,validators
from werkzeug.security import generate_password_hash
from datasource import is_email_duplicate,add_user


class RegistrationForm(FlaskForm):
    username = StringField('使用者名稱',[
        validators.Length(min=4,max=25),
        validators.InputRequired("使用者名稱必需要有資料")
    ])
    email = EmailField('電子郵件',[
        validators.Length(min=6, max=35),
        validators.InputRequired('email必需有資料')
    ])
    password = PasswordField('密碼',[
        validators.DataRequired('密碼必需有資料'),
        validators.EqualTo('confirm',message="密碼驗証不相同")
    ])
    confirm =PasswordField('再次確認密碼',[
        validators.InputRequired('再次確認密碼')
    ])

@auth.route('/regist',methods=['GET','POST'])
def regist():
    form = RegistrationForm(request.form)
    if request.method == "POST" and form.validate(): 
        name = form.username.data
        email = form.email.data
        password = form.password.data
        password_hash = generate_password_hash(password=password,method='pbkdf2:sha256',salt_length=8)
        print(password_hash)        
        if not is_email_duplicate(email):
            #email沒有重覆
            if add_user(name,email,password_hash):
                return redirect(url_for('auth.success'))
            else:
                print("加入失敗")
        else:
            print('email有重覆')
        
    return render_template('auth/registration.j2',form=form)