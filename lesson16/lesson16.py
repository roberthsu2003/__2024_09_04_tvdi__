from flask import Flask,render_template,request,redirect,url_for
import datasource
from flask_wtf import FlaskForm
from wtforms import EmailField,BooleanField,PasswordField,SubmitField
from wtforms.validators import DataRequired,Length
import secrets

app = Flask(__name__)
app.config['SECRET_KEY'] = secrets.token_hex(16)

@app.route("/")
def index():
    return render_template('index.j2')

@app.route("/product")
def product():
    cities:list[dict] = datasource.get_cities()
    page = request.args.get('page',1, type=int)
    per_page = 10
    start = (page-1) * per_page
    end = start + per_page
    total_pages = (len(cities) + per_page - 1 ) // per_page
    items_on_page = cities[start:end]
    return render_template('product.j2',
                           items_on_page=items_on_page,
                           total_pages=total_pages,
                           page = page)

@app.route("/pricing")
def pricing():
    cities:list[dict] = datasource.get_cities()
    page = request.args.get('page',1, type=int)
    per_page = 6
    start = (page-1) * per_page
    end = start + per_page
    total_pages = (len(cities) + per_page - 1 ) // per_page
    items_on_page = cities[start:end]
    return render_template('pricing.j2',
                            items_on_page=items_on_page,
                            total_pages=total_pages,
                            page = page) 

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

@app.route("/success")
def success():
    return "<h1>登入成功</h1>"