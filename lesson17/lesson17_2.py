from dash import Dash,html,dcc,callback,Input, Output,dash_table,_dash_renderer
import pandas as pd
import plotly.express as px
import dash_mantine_components as dmc
_dash_renderer._set_react_version("18.2.0")

df = pd.read_csv('https://raw.githubusercontent.com/plotly/datasets/master/gapminder_unfiltered.csv')

app = Dash(__name__,external_stylesheets=dmc.styles.ALL)

#radio button要顯示的資料
radio_data = [['pop','人口'],['lifeExp','平均壽命'],['gdpPercap','人均gdp']]

#selected要的資料
selected_data = [{'value':value,'label':value} for value in df.country.unique()]

#table要顯示的資料
# elements = [
#     {"position": 6, "mass": 12.011, "symbol": "C", "name": "Carbon"},
#     {"position": 7, "mass": 14.007, "symbol": "N", "name": "Nitrogen"},
#     {"position": 39, "mass": 88.906, "symbol": "Y", "name": "Yttrium"},
#     {"position": 56, "mass": 137.33, "symbol": "Ba", "name": "Barium"},
#     {"position": 58, "mass": 140.12, "symbol": "Ce", "name": "Cerium"},
#     {"position": 58, "mass": 140.12, "symbol": "Ce", "name": "Cerium"},
#     {"position": 58, "mass": 140.12, "symbol": "Ce", "name": "Cerium"},
#     {"position": 58, "mass": 140.12, "symbol": "Ce", "name": "Cerium"},
#     {"position": 58, "mass": 140.12, "symbol": "Ce", "name": "Cerium"},
#     {"position": 58, "mass": 140.12, "symbol": "Ce", "name": "Cerium"},
#     {"position": 58, "mass": 140.12, "symbol": "Ce", "name": "Cerium"},
#     {"position": 58, "mass": 140.12, "symbol": "Ce", "name": "Cerium"},
# ]

# rows = [
#     dmc.TableTr(
#         [
#             dmc.TableTd(element["position"]),
#             dmc.TableTd(element["name"]),
#             dmc.TableTd(element["symbol"]),
#             dmc.TableTd(element["mass"]),
#         ]
#     )
#     for element in elements
# ]

# head = dmc.TableThead(
#     dmc.TableTr(
#         [
#             dmc.TableTh("Element Position"),
#             dmc.TableTh("Element Name"),
#             dmc.TableTh("Symbol"),
#             dmc.TableTh("Atomic Mass"),
#         ]
#     )
# )

#body = dmc.TableTbody(rows)
#caption = dmc.TableCaption("Some elements from periodic table")

#只顯示台灣的資料
dff = df[df.country == 'Taiwan']
pop_diff = dff[['country', 'year', 'pop']]
elements = pop_diff.to_dict('records')

rows = [
    dmc.TableTr(
        [
            dmc.TableTd(element["country"]),
            dmc.TableTd(element["year"]),
            dmc.TableTd(element["pop"]),
        ]
    )
    for element in elements
]

head = dmc.TableThead(
    dmc.TableTr(
        [
            dmc.TableTh("國家"),
            dmc.TableTh("年份"),
            dmc.TableTh("人口"),
        ]
    )
)

body = dmc.TableTbody(rows)

caption = dmc.TableCaption("Taiwan 年份,人口")
app.layout = dmc.MantineProvider(
    [
    
        dmc.Container(        
            dmc.Title(f"世界各國人口,壽命,gdp統計數字", order=2),
            fluid=True,
            ta='center',
            my=30  
        )
    ,
        dmc.Flex(
            [
                dmc.Stack(
                    [
                        #dcc.RadioItems(['pop','lifeExp','gdpPercap'],value='pop',inline=True,id='radio_item')
                        dmc.RadioGroup(
                            children=dmc.Group([dmc.Radio(l, value=k) for k, l in radio_data], my=10),
                            id="radio_item",
                            value="pop",
                            label="請選擇查詢的種類",
                            size="md",
                            mb=10,
                        )
        
                    , 
                        #dcc.Dropdown(df.country.unique(),value='Taiwan',id='dropdown-selection')
                        dmc.Select(
                            label="請選擇國家",
                            placeholder="請選擇1個",
                            id="dropdown-selection",
                            value="Taiwan",
                            data=selected_data,
                            w=200,
                            mb=10,
                        )
                    ],
                    
                )
            ,
                
                #dash_table.DataTable(data=[],page_size=10,id='datatable',columns=[])
                dmc.ScrollArea(
                    dmc.Table(
                        [head, body, caption],
                        w='100%'
                    ),
                    h=300,
                    w='50%'
                )

                
                

            ],
            direction={"base": "column", "sm": "row"},
            gap={"base": "sm", "sm": "lg"},
            justify={"base": "center"},
            

        )
    ,
    #dcc.Graph(id='graph-content')
        dmc.Container(
           dcc.Graph(id='graph-content') 
        )
    ]
)

#圖表顯示的事件
@callback(    
    Output('graph-content','figure'),
    Input('dropdown-selection','value'),
    Input('radio_item','value')
    
)
def update_graph(country_value,radio_value):
    dff = df[df.country == country_value]
    print(radio_value)
    if radio_value == "pop":
        title = f'{country_value}:人口成長圖表'
    elif radio_value == "lifeExp":
        title = f'{country_value}:預期壽命'
    elif radio_value == 'gdpPercap':
        title = f'{country_value}:人均GDP'

    return px.line(dff,x='year',y=radio_value,title=title)

#表格顯示的事件
# @callback(    
#     Output('datatable','data'),
#     Output('datatable','columns'),    
#     Input('dropdown-selection','value'),
#     Input('radio_item','value') 
# )
# def update_table(country_value,radio_value):
#     dff = df[df.country == country_value]
#     columns = [
#         {'id':'country','name':'country'},
#         {'id':'year','name':'year'}        
#     ]
#     if radio_value == 'pop':
#         columns.append({'id':'pop','name':'pop'})
#     elif radio_value == 'lifeExp':
#         columns.append({'id':'lifeExp','name':'lifeExp'})
#     elif radio_value == 'gdpPercap':
#         columns.append({'id':'gdpPercap','name':'gdpPercap'})

#     return dff.to_dict('records'),columns
    

if __name__ == '__main__':
    app.run(debug=True)