from dash import Dash,html,dcc,callback,Input,Output,dash_table,_dash_renderer
import pandas as pd
import plotly.express as px
import dash_mantine_components as dmc
from dash_iconify import DashIconify
import sqlite3
import plotly.graph_objs as go

_dash_renderer._set_react_version("18.2.0")



df = pd.read_csv('NewTable_202412100949.csv')
if 'Date' in df.columns:
    df['Date'] = pd.to_datetime(df['Date'])
else:
    raise ValueError("The Date column is missing")



df['Days'] = (df['Date']-df['Date'].min()).dt.days
df['Date_str'] = df['Date'].dt.strftime('%Y-%m-%d')



app1 = Dash(__name__,external_stylesheets=dmc.styles.ALL,requests_pathname_prefix="/dash/")

# radio資料
radio_data = [['Close', "收盤價"], ['Open', "開盤價"], ['High', "最高價"], ['Low', "最低價"], ['Volume', "成交量"]]
radio_data_dict = {k: l for k, l in radio_data}
methods = [
    {'key': 'rsi', 'name': 'RSI'},
    {'key': 'sma', 'name': 'SMA'},
    {'key': 'macd', 'name': 'MACD'}
]



# 預設的 radio 項目為 'Open' (開盤價)
default_radio_value = 'Close'


# 應用的布局
app1.layout = dmc.MantineProvider(
    dmc.AppShell(
        children=[
            dmc.AppShellHeader(
                dmc.NavLink(
                    label='台積電股票分析',
                    leftSection=DashIconify(icon="tabler:gauge"),
                    active=True,
                    variant="filled",
                    color="blue",
                    id="school_icon",
                    h=70,
                    href='/',
                    refresh=True
                ),
            ),
            dmc.AppShellMain(
                [
                    dmc.Container(
                        dmc.Title(f'台積電股票分析', order=2),
                        fluid=True,
                        ta="center",
                        p=30
                    ),
                    dmc.Flex(
                        [
                            dmc.Stack(
                                children=[
                                    dmc.RadioGroup(
                                        id="radio_item",
                                        value=default_radio_value,
                                        children=[
                                            dmc.Radio(label=name, value=key)
                                            for key, name in radio_data_dict.items()
                                        ],
                                        style={"width": "200px","margin": "0 auto"}  # 調整寬度
                                    ),
                                    dmc.Select(
                                        id="dropdown-selection",
                                        placeholder="選擇分析方法",
                                        value=methods[0]['key'],  # 預設為第一個分析方法
                                        data=[{'label': m['name'], 'value': m['key']} for m in methods],
                                        style={"width": "200px","margin": "0 auto"}  # 調整寬度
                                    ),
                                ],
                                gap="lg",
                                style={"flex": 1,}
                            ),
                            dmc.Stack(
                                children=[
                                    dash_table.DataTable(
                                        id="datatable",
                                        columns=[],
                                        page_size=10,
                                        style_table={'height': '300px', 'overflowY': 'auto'},
                                        style_header={'backgroundColor': 'lightgreen', 'fontWeight': 'bold'},
                                        style_cell={'textAlign': 'center', 'width': '300px'},
                                    ),
                                ],
                                gap="lg",
                                style={"flex": 2, "margin-left": "0px"},  # 將表格寬度比例設定為 2
                                
                            )
                        ],
                        direction="row",  # 水平排列
                        gap={"base": "sm", "sm": "lg"},
                        justify="flex-start",  # 元素均分空間
                        pr=300
                    ),
                    dmc.Flex(
                        [
                            dmc.Container(
                                dcc.Graph(id="graph-content1", style={"height": "400px"})
                            ),
                            dmc.Container(
                                dcc.Graph(id="fig1-content", style={"height": "400px"})
                            ),
                        ],
                        direction="row",  # 圖表水平排列
                        gap="lg",
                        
                        pr=150
                    )
                ]
            )
        ]
    )
)

# 更新圖表及表格的回呼
@callback(
    [Output('graph-content1', 'figure'),
     Output('fig1-content', 'figure'),
     Output('datatable', 'data'),
     Output('datatable', 'columns')],  # 更新表格的欄位
    [Input('radio_item', 'value'),
     Input('dropdown-selection','value')]
)
def update_content(radio_value,selected_method):
    # 更新圖表
    sorted_df = df.sort_values('Date')
    title = f'{radio_data_dict[radio_value]}'
    fig = px.line(data_frame=sorted_df, x="Date", y=radio_value, title=title)

    
    
# 根據選擇的分析方法計算數據
    if selected_method == "rsi":
        data = calculate_rsi(sorted_df.copy())
        y_col = "RSI"
    elif selected_method == "sma":
        data = calculate_sma(sorted_df.copy())
        y_col = "SMA"
    elif selected_method == "macd":
        data = calculate_macd(sorted_df.copy())
        y_col = "MACD"
    else:
        data = None
        y_col = None

    # if selected_method == "macd":
    #     print("MACD DataFrame:")
    #     print(data[['Date', 'MACD', 'Signal_Line']].head())
    # elif selected_method in ["rsi", "sma"]:
    #     print(f"{selected_method.upper()} DataFrame:")
    #     print(data[['Date', y_col]].head())




    # 主圖（分析結果）
    if selected_method == "macd":
        fig1 = px.line(data, x="Date", y=["MACD", "Signal_Line"], title=f"MACD",labels={
        "variable": "標籤名稱",  # 將 variable 替換為自定義名稱
         # 替換其他標籤名稱（可選）
    })
    elif selected_method == "sma":
        data = calculate_sma(data)  # 保證 data 還是 DataFrame
        fig1 = px.line(data, x="Date", y=["SMA_short", "SMA_long"], title="SMA",labels={
        "variable": "標籤名稱"})
        
    elif selected_method == "rsi":
        data = calculate_rsi(data)  # 保證 data 還是 DataFrame
        fig1 = px.line(data, x="Date", y=["RSI"], title="RSI",labels={
        "variable": "標籤名稱"})
    else:
        fig1 = go.Figure()



    filtered_df = df[['Date_str', radio_value]]
    table_data = filtered_df.to_dict('records')
    
    columns = [
        {"name": "日期", "id": "Date_str"},
        {"name": radio_data_dict[radio_value], "id": radio_value}
    ]

    # 返回圖表、表格資料和欄位
    return fig, fig1, table_data, columns







def calculate_rsi(data):
    delta = data['Close'].diff()
    window = 14
    gain = delta.where(delta > 0, 0)
    loss = -delta.where(delta < 0, 0)
    avg_gain = gain.rolling(window=window).mean()
    avg_loss = loss.rolling(window=window).mean()
    rs = avg_gain / avg_loss
    data['RSI'] = 100 - (100 / (1 + rs))
    return data


def calculate_sma(data):
    window1 = 20
    window2 = 90 
    data['SMA_short'] = data['Close'].rolling(window=window1).mean()
    data['SMA_long'] = data['Close'].rolling(window=window2).mean()
    return data


def calculate_macd(data):
    short_window = 12
    long_window = 26
    signal_window = 9
    data['MACD'] = data['Close'].ewm(span=short_window, adjust=False).mean() - data['Close'].ewm(span=long_window, adjust=False).mean()
    data['Signal_Line'] = data['MACD'].ewm(span=signal_window, adjust=False).mean()
    return data




if __name__ == '__main__':
    app1.run(debug=True)