from . import auth

@auth.route('/regist')
def regist():
    return "<h1>Regist</h1>"