from . import auth
from flask import redirect,session

@auth.route('/logout')
def logout():
    session.pop('username',None)
    return redirect('/')