from . import auth

@auth.route('/success')
def success():
    return "<h1>註冊成功</h1>"