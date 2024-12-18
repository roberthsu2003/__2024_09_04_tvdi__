from dash import Dash, html, dcc, callback, Input, Output, dash_table, _dash_renderer
import pandas as pd
import plotly.express as px
import dash_mantine_components as dmc
_dash_renderer._set_react_version("18.2.0")

# 記得要先更換csv路徑
file_path = r'C:\\Users\\user\\Documents\\GitHub\\python_windows\\專案\\2023-2009pet_data.csv'

try:
    df = pd.read_csv(file_path)
    print("文件成功讀取！")
    print(df.columns)  # 檢查列名
except FileNotFoundError:
    print(f"找不到文件：{file_path}")
    raise
except KeyError as e:
    print(f"列名錯誤：{e}")
    raise

app = Dash(__name__, external_stylesheets=dmc.styles.ALL)

# radio button的資料改為下拉選單資料
combobox_data = [
    {"value": "Registrations", "label": "登記數"},
    {"value": "Deregistrations", "label": "註銷數"},
    {"value": "Neutered", "label": "絕育數"}
]

# selected要的資料
selected_data = [{'value': value, 'label': value} for value in df.County.unique()]

# 只顯示台灣的資料
dff = df[df.County == 'Taiwan']
Registrations_diff = dff[['County', 'Year', 'Registrations']]
elements = Registrations_diff.to_dict('records')

rows = [
    dmc.TableTr(
        [
            dmc.TableTd(element["County"]),
            dmc.TableTd(element["Year"]),
            dmc.TableTd(element["Registrations"]),
        ]
    )
    for element in elements
]

head = dmc.TableThead(
    dmc.TableTr(
        [
            dmc.TableTh("年份"),
            dmc.TableTh("縣市"),
            dmc.TableTh("登記數"),
            dmc.TableTh("註銷數"),
            dmc.TableTh("絕育數"),
        ]
    )
)

body = dmc.TableTbody(rows)
caption = dmc.TableCaption("Taiwan 年份,登記數量")

app.layout = dmc.MantineProvider(
    [
        dmc.Container(
            dmc.Title(f"各縣市 登記數、註銷數、絕育數 數據", order=2),
            fluid=True,
            ta='center',
            my=30
        ),
        dmc.Flex(
            [
                dmc.Stack(
                    [
                        dmc.Select(
                            label="請選擇查詢的種類",
                            placeholder="請選擇一項",
                            id="combobox-item",
                            value="Registrations",
                            data=combobox_data,
                            w=200,
                            mb=10
                        ),
                        dmc.Select(
                            label="請選擇縣市",
                            placeholder="請選擇1個",
                            id="dropdown-selection",
                            value="Taiwan",
                            data=selected_data,
                            w=200,
                            mb=10
                        )
                    ],
                ),
                dmc.ScrollArea(
                    dash_table.DataTable(
                        id="data-table",  # 表格 ID
                        columns=[
                            {"name": "年份", "id": "Year"},
                            {"name": "縣市", "id": "County"},
                            {"name": "登記數", "id": "Registrations"},
                            {"name": "註銷數", "id": "Deregistrations"},
                            {"name": "絕育數", "id": "Neutered"}
                        ],
                        style_table={'height': '300px', 'overflowY': 'auto'},
                        style_header={'fontWeight': 'bold'},
                        style_cell={'textAlign': 'center'}
                    ),
                    h=300,
                    w='70%'
                )
            ],
            direction={"base": "column", "sm": "row"},
            gap={"base": "sm", "sm": "lg"},
            justify={"base": "center"},
        ),
        dmc.Container(
            dcc.Graph(id='graph-content')
        )
    ]
)

# 圖表顯示的事件
@callback(
    Output('graph-content', 'figure'),
    Output('data-table', 'data'),  # 更新 DataTable 的資料
    Input('dropdown-selection', 'value'),
    Input('combobox-item', 'value')
)
def update_content(county_value, combobox_value):
    # 篩選指定縣市的數據
    dff = df[df.County == county_value]

    # 動態設定 Y 軸欄位、標題和 legend 名稱
    if combobox_value == "Registrations":
        y_column = 'Registrations'
        title = f'{county_value}: 登記數歷年趨勢'
        legend_name = '登記數'
    elif combobox_value == "Deregistrations":
        y_column = 'Deregistrations'
        title = f'{county_value}: 註銷數歷年趨勢'
        legend_name = '註銷數'
    elif combobox_value == "Neutered":
        y_column = 'Neutered'
        title = f'{county_value}: 絕育數歷年趨勢'
        legend_name = '絕育數'

    # 更新圖表
    fig = px.line(
        dff,
        x='Year',
        y=y_column,
        title=title,
        labels={y_column: legend_name}
    )
    fig.update_traces(name=legend_name)

    # 更新表格數據（保留所有所需欄位）
    table_data = dff[["Year", "County", "Registrations", "Deregistrations", "Neutered"]].to_dict('records')

    return fig, table_data


if __name__ == '__main__':
    app.run(debug=True)
