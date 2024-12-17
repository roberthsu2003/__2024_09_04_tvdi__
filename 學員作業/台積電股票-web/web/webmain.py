from dash import Dash,html,dcc,callback,Input,Output,dash_table,_dash_renderer
import pandas as pd
import plotly.express as px
import dash_mantine_components as dmc
from dash_iconify import DashIconify
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
                            dmc.RadioGroup(
                                children=
                                    [   dmc.Group([dmc.Radio(l, value=k) for k, l in radio_data[:3]], my=10),  # 第一行
                                        dmc.Group([dmc.Radio(l, value=k) for k, l in radio_data[3:]], my=10)   # 第二行
                                     ],
                                id="radio_item",
                                value=default_radio_value,  # 預設為開盤價
                                label="請選擇想了解的資料",
                                size='md',
                                mb=10
                            ),
                            dash_table.DataTable(
                                id="datatable",
                                columns=[],
                                page_size=10,
                                style_table={'height': '300px', 'overflowY': 'auto'},
                                style_header={'backgroundColor': 'lightgreen', 'fontWeight': 'bold'},
                                style_cell={'textAlign': 'center', 'width': '300px'},
                            ),
                        ],
                        direction={"base": "column", "sm": "row"},
                        gap={"base": "sm", "sm": "lg"},
                        justify={"base": "center"}
                    ),
                    dmc.Container(
                        dcc.Graph(id="graph-content")
                    )
                ]
            )
        ]
    )
)

# 更新圖表及表格的回呼
@callback(
    [Output('graph-content', 'figure'),
     Output('datatable', 'data'),
     Output('datatable', 'columns')],  # 更新表格的欄位
    [Input('radio_item', 'value')]
)
def update_content(radio_value):
    # 更新圖表
    sorted_df = df.sort_values('Date')
    title = f'{radio_data_dict[radio_value]}'
    fig = px.line(data_frame=sorted_df, x="Date", y=radio_value, title=title)

    # 更新表格資料
    columns = [
        {"name": "日期", "id": "Date_str"},
        {"name": radio_data_dict[radio_value], "id": radio_value}  # 根據選擇的 radio_value 更新第二欄
    ]
    
    filtered_df = df[['Date_str', radio_value]]
    table_data = filtered_df.to_dict('records')
    
    print(table_data)
    
    return fig, table_data, columns


if __name__ == '__main__':
    app1.run(debug=True)