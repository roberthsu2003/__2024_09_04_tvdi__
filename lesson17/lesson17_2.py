from dash import Dash,html,dcc,callback,Input, Output,dash_table,_dash_renderer
import pandas as pd
import plotly.express as px
import dash_mantine_components as dmc

_dash_renderer._set_react_version("18.2.0")

df = pd.read_csv('https://raw.githubusercontent.com/plotly/datasets/master/gapminder_unfiltered.csv')

dash_app = Dash(external_stylesheets=dmc.styles.ALL,requests_pathname_prefix="/dash/")

#radio button要顯示的資料
radio_data = [['pop','人口'],['lifeExp','平均壽命'],['gdpPercap','人均gdp']]

#selected要的資料
selected_data = [{'value':value,'label':value} for value in df.country.unique()]



caption = dmc.TableCaption("Taiwan 年份,人口")
dash_app.layout = dmc.MantineProvider(
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
                    children = [],
                    id = 'table_scroll',
                    h=300,
                    w='300'
                )

            ],
            direction={"base": "row"},
            gap={"base": "50"},
            justify={"base": "center"},
            

        )
    ,
    #dcc.Graph(id='graph-content')
        dmc.Container(
            dmc.LineChart(
                id='graph-content',
                h = 300,
                dataKey='year',
                data=[],
                series=[{"name":"pop","color":"indigo.6"}]     
            ),
            mt=50,
            mb=50
        )
    ]
)

#圖表顯示的事件
@callback(    
    Output('graph-content','data'),
    Output('graph-content','series'),
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

    return dff[['year',radio_value]].to_dict('records'),[{"name":radio_value,"color":"indigo.6"}]

#表格顯示的事件
@callback(    
    Output('table_scroll','children'),    
    Input('dropdown-selection','value'),
    Input('radio_item','value') 
)
def update_table(country_value,radio_value):
    #只顯示台灣的資料
    dff = df[df.country == country_value]
    pop_diff = dff[['country', 'year', radio_value]]
    elements = pop_diff.to_dict('records')

    rows = [
        dmc.TableTr(
            [
                dmc.TableTd(element["country"]),
                dmc.TableTd(element["year"]),
                dmc.TableTd(element[radio_value]),
            ]
        )
        for element in elements
    ]
    if radio_value == 'pop':
        theme = '人口'
    elif radio_value == "lifeExp":
        theme = '人均壽命'
    elif radio_value == 'gdpPercap':
        theme = 'GDP' 

    head = dmc.TableThead(
        dmc.TableTr(
            [
                dmc.TableTh("國家"),
                dmc.TableTh("年份"),
                dmc.TableTh(theme),
            ]
        )
    )

    body = dmc.TableTbody(rows)


    return dmc.Table([head, body, caption],w='300')
    

if __name__ == '__main__':
    app.run(debug=True)