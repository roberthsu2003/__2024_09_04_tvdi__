from dash import Dash,html,dcc,callback,Input, Output
import pandas as pd
import plotly.express as px

df = pd.read_csv('https://raw.githubusercontent.com/plotly/datasets/master/gapminder_unfiltered.csv')

app = Dash(__name__)

app.layout = html.Div(
    [
    html.H1("Dash App的標題",style={"textAlign":'center'}),
    dcc.Dropdown(df.country.unique(),value='Taiwan',id='dropdown-selection'),
    dcc.Graph(id='graph-content')
    ])

@callback(
    Output('graph-content','figure'),
    Input('dropdown-selection','value')
)
def update_graph(value):
    dff = df[df.country == value]
    return px.line(dff,x='year',y='pop',title=f'{value}:人口成長圖表')
    

if __name__ == '__main__':
    app.run(debug=True)