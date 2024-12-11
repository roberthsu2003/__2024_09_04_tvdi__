from flask import render_template
from . import auth

@auth.route('/registration')
def registration():
    return render_template('auth/registration.j2')