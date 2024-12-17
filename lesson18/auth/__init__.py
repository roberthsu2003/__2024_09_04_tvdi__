from flask import Blueprint
auth = Blueprint('auth',__name__)

@auth.route('/login')
def login():
    return "<h1>Hello! World!</h1>"