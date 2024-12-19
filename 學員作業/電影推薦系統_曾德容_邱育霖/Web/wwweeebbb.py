import os
from flask import Flask, render_template, request, redirect, url_for, session
import dash
import dash_bootstrap_components as dbc
from dash import html, dcc
from dash.dependencies import Input, Output

app = Flask(__name__)
app.secret_key = 'your_secret_key'

# 推薦電影資料 - 移到最前面
RECOMMENDED_MOVIES = [
    {
        "name": "AI與小愛",
        "image_path": "/static/Images/AI_and_ai.jpg"
    },
    {
        "name": "地獄律師",
        "image_path": "/static/Images/lawyerhell.jpg"
    },
    # 其他電影資料...
]

# Dash 設定
dash_app = dash.Dash(__name__,
                     server=app,
                     routes_pathname_prefix='/dash/',
                     external_stylesheets=[dbc.themes.BOOTSTRAP])

# 重點在這裡：為 Dash 應用程式設置佈局
dash_app.layout = html.Div([
    html.H1('電影選擇'),
    dcc.Dropdown(
        id='movie-dropdown',
        options=[
            {'label': movie['name'], 'value': movie['name']} 
            for movie in RECOMMENDED_MOVIES
        ],
        placeholder='選擇一部電影'
    ),
    html.Div(id='dropdown-output')
])

# 初始化待播清單和觀看紀錄
watchlist = []
played_list = [
    "在小A的世界裡迷路",
    "三生三世三十場考試",
    # 其他觀看紀錄...
]

# 登入頁面
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        # 這裡應該有登入驗證的邏輯
        if username == '1234' and password == '5678':
            session['logged_in'] = True
            return redirect(url_for('index'))
        else:
            return render_template('login.j2', error='Invalid username or password')
    return render_template('login.j2')

# 首頁
@app.route('/')
def index():
    if 'logged_in' not in session:
        return redirect(url_for('login'))
    return render_template(
        'index.j2',
        recommended_movies=RECOMMENDED_MOVIES,
        watchlist=watchlist,
        played_list=played_list
    )

# Dash 回調函數
@dash_app.callback(
    Output('dropdown-output', 'children'),
    Input('movie-dropdown', 'value')
)
def update_output(value):
    if value:
        return f"您選擇了：{value}"
    return "請選擇一部電影"

# 運行應用程式
if __name__ == '__main__':
    app.run(debug=True)