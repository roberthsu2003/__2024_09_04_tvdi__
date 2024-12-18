from dash import Dash, Input, Output, dcc, html, callback, ctx, ALL,dash_table,_dash_renderer
import dash_mantine_components as dmc
from dash_iconify import DashIconify
import pandas as pd
import chardet
import plotly.express as px
import plotly.graph_objects as go
_dash_renderer._set_react_version("18.2.0")
# 讀取檔案編碼
file_path = 'Gogoro_站點整理.csv'
with open(file_path, 'rb') as file:
    result = chardet.detect(file.read())
detected_encoding = result['encoding']

# 讀取 CSV 資料
df = pd.read_csv(file_path, encoding=detected_encoding)


# 資料清理
df = df.dropna(subset=['city', 'dist', 'lat', 'lon'])  # 移除缺失值
df['city'] = df['city'].astype(str).str.strip()
df['dist'] = df['dist'].astype(str).str.strip()

# 城市下拉選單資料
city_options = [{'value': city, 'label': city} for city in df['city'].unique()]

def get_districts(city):
    """取得該城市的區域列表"""
    return [{'value': dist, 'label': dist} for dist in df[df['city'] == city]['dist'].unique()]

# 初始化 Dash App
app1 = Dash(__name__,external_stylesheets=dmc.styles.ALL,requests_pathname_prefix="/dash/")

# App Layout
app1.layout = dmc.MantineProvider(
    dmc.AppShell(
        children=[
            dmc.AppShellHeader(
                dmc.NavLink(
                    label="城市與區域選單",
                    leftSection=DashIconify(icon="tabler:map-pin"),
                    active=True,
                    variant="filled",
                    color="blue",
                    id="app_header",
                    href='/',
                    refresh=True
                ),
                h=70
            ),
            dmc.AppShellMain([
                dmc.Container([
                    dmc.Title("城市與區域選擇系統", order=2, ta="center", my=20),
                    dmc.Flex([
                        dmc.Select(
                            label="選擇城市",
                            id="city-dropdown",
                            placeholder="請選擇城市",
                            value=city_options[0]['value'] if city_options else None,
                            data=city_options,
                            w=300
                        ),
                        dmc.Select(
                            label="選擇區域",
                            id="dist-dropdown",
                            placeholder="請先選擇城市",
                            value=None,
                            data=[],
                            w=300
                        ),
                    ], gap="md", justify="center", my=20),
                    dmc.ScrollArea(
                        dmc.Table(
                            id='data-table',
                            striped=True,
                            highlightOnHover=True
                        ),
                        h=300
                    ),
                    dcc.Graph(id="map", style={"height": "500px"})
                ])
            ])
        ]
    )
)

# 回調：更新區域選單
@callback(
    Output('dist-dropdown', 'data'),
    Output('dist-dropdown', 'value'),
    Input('city-dropdown', 'value')
)
def update_districts(selected_city):
    if not selected_city:
        return [], None
    districts = get_districts(selected_city)
    return districts, districts[0]['value'] if districts else None

# 回調：更新表格
@callback(
    Output('data-table', 'children'),
    Input('city-dropdown', 'value'),
    Input('dist-dropdown', 'value')
)
def update_table(selected_city, selected_dist):
    filtered_df = df[(df['city'] == selected_city) & (df['dist'] == selected_dist)]
    
    if filtered_df.empty:
        return dmc.TableThead(dmc.TableTr([
            dmc.TableTh("站點名稱"), dmc.TableTh("地址"), dmc.TableTh("地圖")
        ]))
    
    rows = [
        dmc.TableTr([
            dmc.TableTd(row['sitename']),
            dmc.TableTd(row['address']),
            dmc.TableTd(
                dmc.Button(
                    "開啟地圖",
                    id={"type": "map-button", "index": idx},
                    variant="light",
                    leftSection=DashIconify(icon="tabler:map-pin")
                )
            )
        ]) for idx, (_, row) in enumerate(filtered_df.iterrows())
    ]
    
    table_header = dmc.TableThead(dmc.TableTr([
        dmc.TableTh("站點名稱"), dmc.TableTh("地址"), dmc.TableTh("地圖")
    ]))
    return dmc.Table([table_header, dmc.TableTbody(rows)])

# 回調：顯示地圖
import plotly.graph_objects as go

@callback(
    Output('map', 'figure'),
    Input({'type': 'map-button', 'index': ALL}, 'n_clicks'),
    Input('city-dropdown', 'value'),
    Input('dist-dropdown', 'value')
)
def update_map(button_clicks, selected_city, selected_dist):
    # 篩選資料
    filtered_df = df[(df['city'] == selected_city) & (df['dist'] == selected_dist)]
    
    if filtered_df.empty:
        return go.Figure()

    # 預設顯示第一個站點
    selected_row = filtered_df.iloc[0]

    # 檢查是否有按鈕被點擊
    if ctx.triggered:
        try:
            prop_id = ctx.triggered[0]['prop_id']
            if 'map-button' in prop_id:
                import re
                match = re.search(r'"index":(\d+)', prop_id)
                if match:
                    button_index = int(match.group(1))
                    if 0 <= button_index < len(filtered_df):
                        selected_row = filtered_df.iloc[button_index]
        except Exception as e:
            print(f"Error parsing trigger: {e}")

    # 偵錯：印出經緯度
 

    # 創建地圖
    fig = go.Figure(go.Scattermapbox(
        lon=[selected_row['lon']],  # 使用原始的 lon 和 lat
        lat=[selected_row['lat']],
        mode='markers',
        marker=dict(
            size=14,
            color='red',
            symbol='circle'
        ),
        text=[f"{selected_row['sitename']}<br>{selected_row['address']}"],
        textposition='bottom center',
        hoverinfo='text'
    ))

    # 設定地圖佈局
    fig.update_layout(
        mapbox_style="open-street-map",
        mapbox=dict(
            center=dict(
                lon=selected_row['lon'], 
                lat=selected_row['lat']
            ),
            zoom=15,
            
        ),
        showlegend=False,
        height=500,
        margin={"l":0,"r":0,"t":0,"b":0}
    )

    return fig

if __name__ == '__main__':
    app1.run(debug=True)