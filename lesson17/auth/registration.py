from wtforms import Form,StringField,PasswordField,EmailField,validators
from flask import render_template,request,redirect,url_for,session
from datasource import is_email_duplicate,add_user
from werkzeug.security import generate_password_hash
from . import auth

class RegistrationFrom(Form):
    username = StringField('username',[
        validators.Length(min=4,max=25),
        validators.InputRequired('username必需有資料')
    ])
    
    email = EmailField('Email Address',[
        validators.Length(min=6, max=35),
        validators.InputRequired('email必需有資料')
    ])

    password = PasswordField('New Password',[
        validators.DataRequired('必需有資料'),
        validators.EqualTo('confirm',message='密碼驗証不相同')
    ])

    confirm = PasswordField('Repeat Password')


    

@auth.route('/registration',methods=['GET','POST'])
def register():
    form = RegistrationFrom(request.form)
    if request.method == 'POST' and form.validate():
        name = form.username.data
        email = form.email.data
        password = form.password.data
        if not is_email_duplicate(email):
            password_hash = generate_password_hash(password,method='pbkdf2:sha256',salt_length=8)
            add_user(name,email,password_hash)
        else:
            form.email.errors.append('email有重覆')
            return render_template('auth/registration.j2',form=form) 
        session['username'] = name      
        return redirect(url_for('auth.success'))

    return render_template('auth/registration.j2',form=form)