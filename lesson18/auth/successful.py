from . import auth
from flask import render_template

@auth.route('/success')
def success():
    return render_template('auth/successful.j2')