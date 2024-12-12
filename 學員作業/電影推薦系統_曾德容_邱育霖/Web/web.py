import os
import dash
import dash_bootstrap_components as dbc
from dash import html, dcc
from dash.dependencies import Input, Output
import flask
from flask import render_template, request, jsonify

# 創建 Flask 伺服器
server = flask.Flask(__name__)

# 推薦電影資料
RECOMMENDED_MOVIES = [
    {
        "name": "AI與小愛",
        "image_path": "/static/Images/AI_and_ai.jpg"
    },
    {
        "name": "地獄律師",
        "image_path": "/static/Images/lawyerhell.jpg"
    },
    {
        "name": "圖書館裡的妖精",
        "image_path": "/static/Images/library.jpg"
    },
    {
        "name": "鋼彈吊單槓",
        "image_path": "/static/Images/gandam.jpg"
    },
    {
        "name": "以鵝傳鵝",
        "image_path": "/static/Images/goose.jpg"
    }
]

# 初始化待播清單和觀看紀錄
watchlist = []
played_list = [
    "在小A的世界裡迷路",
    "三生三世三十場考試", 
    "我的模型還活著嗎",
    "南港展覽館官方網站綻放萬丈光芒",
    "紅鯉魚與綠鯉魚與驢"
]

# Flask 路由
@server.route('/')
def index():
    return render_template(
        'index.j2', 
        recommended_movies=RECOMMENDED_MOVIES,
        watchlist=watchlist,
        played_list=played_list
    )

@server.route('/add_to_watchlist', methods=['POST'])
def add_to_watchlist():
    movie = request.json.get('movie')
    if movie and movie not in watchlist:
        watchlist.append(movie)
    return jsonify({"status": "success", "watchlist": watchlist})

# 初始化 Dash 應用程式
app = dash.Dash(__name__, 
                server=server, 
                routes_pathname_prefix='/dash/', 
                external_stylesheets=[dbc.themes.BOOTSTRAP])

# Dash 佈局
app.layout = dbc.Container([
    html.H1("Dash 儀表板"),
    html.Div("這是一個額外的 Dash 儀表板頁面"),
    
    # 可以加入更多 Dash 特有的互動元件
    dcc.Dropdown(
        id='movie-dropdown',
        options=[{'label': movie['name'], 'value': movie['name']} for movie in RECOMMENDED_MOVIES],
        placeholder="選擇一部電影"
    ),
    html.Div(id='dropdown-output')
], fluid=True)

# Dash 回調函數
@app.callback(
    Output('dropdown-output', 'children'),
    Input('movie-dropdown', 'value')
)
def update_output(value):
    if value:
        return f"您選擇了：{value}"
    return "請選擇一部電影"

# 主程式
if __name__ == '__main__':
    server.run(debug=True)