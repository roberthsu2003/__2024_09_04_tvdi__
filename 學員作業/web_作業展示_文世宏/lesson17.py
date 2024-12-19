from flask import Flask,render_template,request,redirect,url_for
from flask_wtf import FlaskForm
from dashtest import app1
from werkzeug.middleware.dispatcher import DispatcherMiddleware
from werkzeug.serving import run_simple
from wtforms import EmailField,BooleanField,PasswordField,SubmitField
from wtforms.validators import DataRequired,Length
import secrets

app = Flask(__name__)
app.config['SECRET_KEY'] = secrets.token_hex(16)

application = DispatcherMiddleware(
    app,
    {"/dashapp": app1.server},
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

class MyForm(FlaskForm):
    email_field = EmailField("Email address",validators=[DataRequired("必需要有資料")])
    password_field = PasswordField("請輸入密碼",validators=[DataRequired("必需要有資料"),Length(5,10)])
    epaper_field = BooleanField("訂閱電子報")
    submit_field = SubmitField("確定送出")

@app.route("/faqs",methods=['POST','GET'])
def faqs():
    myForm = MyForm()

    return render_template('faqs.j2',myform = myForm)

@app.route("/about")
def about():
    return render_template('about.j2')

print(__name__)
if __name__ == "__main__":    
    run_simple("localhost", 8080, application,use_debugger=True,use_reloader=True)