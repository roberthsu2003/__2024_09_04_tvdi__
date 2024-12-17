from . import auth
from flask import render_template

@auth.route('/regist')
def regist():
    return render_template('auth/registration.j2')