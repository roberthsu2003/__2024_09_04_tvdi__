from flask import Flask,render_template,redirect,url_for,request
import datasource
from flask_wtf import FlaskForm
from wtforms import StringField
from wtforms.validators import DataRequired
import secrets


app = Flask(__name__)
app.config['SECRET_KEY'] = secrets.token_hex(16) 

@app.route("/")
def index():
    return render_template('index.j2')

@app.route("/product")
def product():
    cities:list[dict] = datasource.get_cities()
    print(cities)
    return render_template('product.j2')

class MyForm(FlaskForm):
    name = StringField('name',validators=[DataRequired()])
    
@app.route("/pricing", methods=['GET','POST'])
def pricing():
    form = MyForm()
    if form.validate_on_submit():
        name = request.form['name'] 
        return redirect(url_for('success',name=name)) 
    return render_template('pricing.j2',form=form)

@app.route("/faqs")
def faqs():
    return render_template('faqs.j2')

@app.route("/about")
def about():
    return render_template('about.j2')

@app.route("/success")
def success():
    name = request.args.get('name',default="",type=str)
    return render_template('success.j2',name=name) 
