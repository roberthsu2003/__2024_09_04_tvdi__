from flask import Flask,render_template

app = Flask(__name__)

@app.route("/")
def index():
    return render_template('index.j2')

@app.route("/product")
def product():
    return render_template('product.j2')