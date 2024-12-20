from . import auth
from flask import render_template,session,redirect,url_for

@auth.route('/success')
def success():
    name = session.get('username')
    if name is None:
        return redirect(url_for('auth.login'))
    return render_template('auth/successful.j2')