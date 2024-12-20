from . import auth
from flask import render_template,session,redirect,url_for

@auth.route('/logout')
def logout():
    session.pop('username',None)
    return redirect(url_for('index'))