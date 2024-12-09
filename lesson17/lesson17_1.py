from dash import Dash,html,dcc,callback,Input, Output,dash_table
import pandas as pd
import plotly.express as px

df = pd.read_csv('https://raw.githubusercontent.com/plotly/datasets/master/gapminder_unfiltered.csv')

app = Dash(__name__)

app.layout = html.Div(
    [
    html.H1("Dash App的標題",style={"textAlign":'center'}),
    dcc.RadioItems(['pop','lifeExp','gdpPercap'],value='pop',inline=True,id='radio_item'),
    dcc.Dropdown(df.country.unique(),value='Taiwan',id='dropdown-selection'),
    dash_table.DataTable(data=[],page_size=10,id='datatable',columns=[]),
    dcc.Graph(id='graph-content')
    ])

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