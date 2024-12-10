from dash import Dash,html,dcc,callback,Input, Output,dash_table,_dash_renderer
import pandas as pd
import plotly.express as px
import dash_mantine_components as dmc

_dash_renderer._set_react_version('18.2.0')


df = pd.read_csv('https://raw.githubusercontent.com/plotly/datasets/master/gapminder_unfiltered.csv')

app = Dash(__name__,external_stylesheets=dmc.styles.ALL)
radioData = [
    ['pop','人口數'],
    ['lifeExp','壽命'],
    ['gdpPercap','人均GDP']
]

app.layout = dmc.MantineProvider(
    [
        dmc.Title("世界各國人口,壽命,GDP",style={"textAlign":'center'},mb=20,mt=20)
    ,
        #dcc.RadioItems(['pop','lifeExp','gdpPercap'],value='pop',inline=True,id='radio_item'),
        dmc.Container(
            dmc.Grid(
                [
                    dmc.GridCol(
                        [
                            dmc.RadioGroup(
                            children = dmc.Group(
                                [dmc.Radio(l,value=k) for k,l in radioData]
                            ),
                            label = '請選擇查詢種類:',
                            id = 'radio_item',
                            value='pop',
                            size='sm',
                            mb=30
                            )
                        ,
                    #dcc.Dropdown(df.country.unique(),value='Taiwan',id='dropdown-selection'),
                            dmc.Select(
                                label = '請選擇國家',
                                placeholder='--選擇--',
                                id = 'dropdown-selection',
                                value='Taiwan',
                                data=[{'label':name, 'value':name} for name in df.country.unique()],
                                w=200,
                                mb=10
                            )
                        ],
                        span=4
                    )
                ,
                    dmc.GridCol(
                        dash_table.DataTable(data=[],page_size=10,id='datatable',columns=[]),                        
                        span=8
                    )                    
                ]
            ),
            fluid=False
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
    Output('datatable','data'),
    Output('datatable','columns'),    
    Input('dropdown-selection','value'),
    Input('radio_item','value') 
)
def update_table(country_value,radio_value):
    dff = df[df.country == country_value]
    columns = [
        {'id':'country','name':'country'},
        {'id':'year','name':'year'}        
    ]
    if radio_value == 'pop':
        columns.append({'id':'pop','name':'pop'})
    elif radio_value == 'lifeExp':
        columns.append({'id':'lifeExp','name':'lifeExp'})
    elif radio_value == 'gdpPercap':
        columns.append({'id':'gdpPercap','name':'gdpPercap'})

    return dff.to_dict('records'),columns
    

if __name__ == '__main__':
    app.run(debug=True)