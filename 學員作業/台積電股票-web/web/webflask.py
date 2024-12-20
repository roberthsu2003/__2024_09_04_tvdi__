from flask import Flask,render_template,request,redirect,url_for
import flasksource
from flask_wtf import FlaskForm
from wtforms import fields
from wtforms.validators import DataRequired,Length
from werkzeug.middleware.dispatcher import DispatcherMiddleware
from werkzeug.serving import run_simple
import secrets

from webmain import app1
'''
flask 就是一個支援 wsgi的應用程式
真正支援wsgi的程式是 Gunicorn

執行時，在終端機輸入
flask --app 檔案名稱 run --debug

'''
app = Flask(__name__)
app.config['SECRET_KEY'] = secrets.token_hex(16)

application = DispatcherMiddleware(
    app,
    {"/dash": app1.server},
)



@app.route("/")
def index():
    return render_template('index.j2')


@app.route("/product")
def product():
    cities:list[dict] = flasksource.get_cities()
    page = request.args.get('page',1, type=int)
    per_page = 9
    start = (page-1) * per_page
    end = start + per_page
    total_pages = (len(cities) + per_page - 1 ) // per_page
    items_on_page = cities[start:end]
    return render_template('product.j2',
                           items_on_page = items_on_page,
                           total_pages = total_pages,
                           page=page)

@app.route("/pricing")
def pricing():
    cities:list[dict] = flasksource.get_cities()
    page = request.args.get('page',1, type=int)
    per_page = 6
    start = (page-1) * per_page
    end = start + per_page
    total_pages = (len(cities) + per_page - 1 ) // per_page
    items_on_page = cities[start:end]
    return render_template('pricing.j2',
                           items_on_page = items_on_page,
                           total_pages = total_pages,
                           page=page)
    
class MyForm(FlaskForm):
    email_field = fields.EmailField("Email address",validators=[DataRequired("必須要有資料")])
    password_field = fields.PasswordField("請輸入密碼",validators=[DataRequired("必須要有資料"),Length(5,10)])
    e_paper_field = fields.BooleanField("訂閱電子報")
    submit_field = fields.SubmitField("確認送出")

@app.route("/faqs",methods=['POST','GET'])
def faqs():
    myForm = MyForm()
    return render_template('faqs.j2',myForm = myForm)

@app.route("/about")
def about():
    return render_template('about.j2')


@app.route("/success")
def success():
    return "<h1>Log in Successfully</h1>"

if __name__ == "__main__":
    run_simple("localhost", 8080, application,use_debugger=True,use_reloader=True)