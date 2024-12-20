from flask import Flask,render_template,request,redirect,url_for
import datasource
from werkzeug.middleware.dispatcher import DispatcherMiddleware
from werkzeug.serving import run_simple
import secrets
from lesson18_2 import app1
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



@app.route("/about")
def about():
    return render_template('about.j2')

@app.route("/success")
def success():
    return "<h1>登入成功</h1>"

print(__name__)
if __name__ == "__main__":    
    run_simple("localhost", 8080, application,use_debugger=True,use_reloader=True)