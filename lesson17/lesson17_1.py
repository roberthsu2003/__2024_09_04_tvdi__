from dash import Dash,html,dcc,callback,Input, Output,dash_table
import pandas as pd
import plotly.express as px

df = pd.read_csv('https://raw.githubusercontent.com/plotly/datasets/master/gapminder_unfiltered.csv')

app = Dash(__name__)

app.layout = html.Div(
    [
    html.H1("Dash App的標題",style={"textAlign":'center'}),
    dcc.Dropdown(df.country.unique(),value='Taiwan',id='dropdown-selection'),
    dash_table.DataTable(data=[],page_size=10,id='datatable',columns=[
        {'id':'country','name':'country'},
        {'id':'year','name':'year'},
        {'id':'pop','name':'pop'}
        ]),
    dcc.Graph(id='graph-content')
    ])

@callback(    
    Output('graph-content','figure'),     
    Input('dropdown-selection','value')
)
def update_graph(value):
    dff = df[df.country == value]
    return px.line(dff,x='year',y='pop',title=f'{value}:人口成長圖表')

@callback(    
    Output('datatable','data'),     
    Input('dropdown-selection','value')
)
def update_table(value):
    dff = df[df.country == value]
    return dff.to_dict('records')
    

if __name__ == '__main__':
    app.run(debug=True)