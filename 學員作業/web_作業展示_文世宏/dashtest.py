from dash import Dash, html, dcc, callback, Input, Output,_dash_renderer
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
import dash_mantine_components as dmc
from dash_iconify import DashIconify
_dash_renderer._set_react_version("18.2.0")

# 載入數據
try:
    df = pd.read_csv(r'C:\Users\user\Desktop\程式在這裡\GitHub\TVDI_python\testing\readme_proj_2\student_lifestyle_dataset.csv')
    print("數據加載成功")
    print(df.head())  # 檢查數據結構
except Exception as e:
    print("數據加載失敗:", e)

# 準備資料選項
radio_data = [
    ['Study_Hours_Per_Day', '學習時間'],
    ['Extracurricular_Hours_Per_Day', '課外活動時間'],
    ['Sleep_Hours_Per_Day', '睡眠時間'],
    ['Social_Hours_Per_Day', '社交時間']
    ]

# 準備學生選擇下拉選單數據
selected_data = [{'value': value, 'label': value} for value in df['Student_ID'].unique()]

# 初始化 Dash 應用
app1 = Dash(__name__, external_stylesheets=dmc.styles.ALL, requests_pathname_prefix="/dashapp/")

# 應用佈局
app1.layout = dmc.MantineProvider(
    dmc.AppShell(
        children=[
            dmc.AppShellHeader(
                dmc.NavLink(
                    label="學生生活統計",
                    leftSection=DashIconify(icon="tabler:gauge"),
                    active=True,
                    variant="filled",
                    color="blue",
                    id="school_icon",
                    h=70,
                    href='/',
                    refresh=True
                ),
                h=70
            ),
            dmc.AppShellMain(
                [
                    dmc.Container(
                        dmc.Title(f"學生生活統計數據分析", order=2),
                        fluid=True,
                        ta='center',
                        my=30
                    ),
                    dmc.Flex(
                        [
                            dmc.Stack(
                                [
                                    dmc.RadioGroup(
                                        children=dmc.Stack([dmc.Radio(l, value=k) for k, l in radio_data], my=10),
                                        id="radio_item",
                                        value=radio_data[0][0],  # 預設選擇第一個選項
                                        label="請選擇查詢的種類",
                                        size="md",
                                        mb=10
                                    ),
                                    dmc.Select(
                                        label="請選擇學生",
                                        placeholder="請選擇1個",
                                        id="dropdown-selection",
                                        data=selected_data,
                                        value=selected_data[0]['value'] if selected_data else None,  # 預設選擇第一個學生
                                        w=200,
                                        mb=10,
                                    )
                                ],
                            ),
                            dmc.ScrollArea(
                                children=[],
                                h=300,
                                w='50%',
                                id='scrollarea'
                            )
                        ],
                        direction={"base": "column", "sm": "row"},
                        gap={"base": "sm", "sm": "lg"},
                        justify={"base": "center"},
                    ),
                    dmc.Container(
                        dcc.Graph(
                            id='barChart',
                            style={'height': '400px'}),
                        my=50
                    )
                ],
            ),
        ],
        header={'height': 70}
    )
)

# 更新圖表的回調函數
@callback(
    Output('barChart', 'figure'),  # 修改為 barChart 的 figure
    Input('radio_item', 'value')  # 選擇的數據指標
)
def update_graph(selected_metric):
    if not selected_metric:
        # 如果沒有選擇任何指標，返回空白圖表
        return px.bar(title="無數據可顯示")

    # 使用 Plotly Express 繪製長條圖
    fig = px.bar(
        df,
        x='Student_ID',  # X 軸為學生 ID
        y=selected_metric,  # Y 軸為選擇的數據指標
        title=f"學生的 {selected_metric} 數據",
        labels={'Student_ID': '學生 ID', selected_metric: '數值'}
    )

    # 美化圖表
    fig.update_layout(
        xaxis=dict(
            title="學生 ID",
            tickmode="linear",
            tickangle=-45,
            dtick=1,
            range=[1-0.5, 50 + 0.5] 
        ),
        yaxis=dict(
            title="小時"
        ),
        template="plotly_white",
        title_x=0.5,  # 标题居中
        height=500  # 固定图表高度
    )
    fig.update_traces(textfont_size=12, textangle=45, textposition="outside", cliponaxis=False)
    return fig

@callback(
    Output('scrollarea', 'children'),
    [Input('radio_item', 'value')]  # 仅根据选定的指标更新表格
)

def update_table(selected_metric):
    if not selected_metric:
        return dmc.Text("未選擇指標")

    # 检查指标是否存在于数据列中
    if selected_metric not in df.columns:
        return dmc.Text(f"無法顯示數據，因為欄位 {selected_metric} 不存在")

    # 获取所有数据
    table_data = df[['Student_ID', selected_metric,'Stress_Level']].to_dict('records')
    rows = [
        dmc.TableTr(
            [dmc.TableTd(record['Student_ID'], style={"width": "150px"}),
             dmc.TableTd(record[selected_metric], style={"width": "150px"}),
             dmc.TableTd(record['Stress_Level'], style={"width": "150px"})
                         ]
        ) for record in table_data
    ]

    head = dmc.TableThead(
        dmc.TableTr([dmc.TableTh("Student_ID", style={"width": "150px"}),
                     dmc.TableTh(selected_metric, style={"width": "150px"}),
                     dmc.TableTh("Stress_Level", style={"width": "150px"})])
    )
    body = dmc.TableTbody(rows)
    caption = dmc.TableCaption(f"所有學生的 {selected_metric} 統計數據")
    table = dmc.Table([head, body, caption])
    return table



# 啟動應用
if __name__ == '__main__':
    app1.run(debug=True)
