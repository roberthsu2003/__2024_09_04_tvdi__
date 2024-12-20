from flask import Flask,render_template,request,redirect,url_for
from werkzeug.middleware.dispatcher import DispatcherMiddleware
from werkzeug.serving import run_simple
import secrets
from DASH import app1
from auth import auth

app = Flask(__name__)
app.config['SECRET_KEY'] = secrets.token_hex(16)
app.register_blueprint(auth,url_prefix='/auth')


application = DispatcherMiddleware(
    app,
    {"/dash": app1.server},
)

@app.route("/")
def index():
    return render_template('index.j2')

@app.route("/product")
def product():
   
    return render_template('product.j2')

@app.route("/pricing")
def pricing():
    
    return render_template('pricing.j2') 


@app.route("/success")
def success():
    return "<h1>登入成功</h1>"

print(__name__)
if __name__ == "__main__":    
    run_simple("localhost", 8080, application,use_debugger=True,use_reloader=True)