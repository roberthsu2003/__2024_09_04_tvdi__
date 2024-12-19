from dash import Dash,html,dcc,callback,Input,Output,dash_table
import pandas as pd
import plotly.express as px

df = pd.read_csv('https://raw.githubusercontent.com/Austin-Chang-zz/Python_Web/main/HomeWork/sales_orders.csv')

app1 = Dash(__name__,requests_pathname_prefix="/dash/")


# Define the layout
app1.layout = html.Div([
    html.H1("Production Page", style={'textAlign': 'center'}),
    dcc.Markdown("### Check Production Yield Rate & Thru Put of Customer's Order for Each Sales",style={'textAlign':'center'}),
    dcc.RadioItems(['yield_rate','thru_put'],value='yield_rate',inline=True,id='radio_item'),
    dcc.Dropdown(df.sales_name.unique(),value="Alice",id='dropdown-selection'),
    dash_table.DataTable(data=[],page_size=10,id='datatable',columns=[]),
    dcc.Graph(id='graph-content') 
])

# Event for showing the graph
@callback(
    Output('graph-content','figure'),
    Input('dropdown-selection','value'),
    Input('radio_item','value')
    
    
)

def update_graph(sales_name_value,radio_value):
    dff = df[df.sales_name == sales_name_value]
    if radio_value == 'yield_rate':
        title = f'{sales_name_value}: Yield Rate Chart'
    elif radio_value == 'thru_put':
        title = f'{sales_name_value}: Through Put Chart'
        
    return px.scatter(dff, x='order_date',y=radio_value,title=title)

# Event for showing the table
@callback(
    Output('datatable','data'),
    Output('datatable','columns'),
    Input('dropdown-selection','value'),
    Input('radio_item','value')
)

def update_table(sales_name_value,radio_value):
    dff = df[df.sales_name == sales_name_value]
    columns = [
        {'id':'sales_name','name':'sales_name'},
        {'id':'customer_id','name':'customer_id'},
        {'id':'order_date','name':'order_date'},
        {'id':'deliver_date','name':'deliver_date'},
        {'id':'factory','name':'factory'}
    ]
    if radio_value == 'yield_rate':
        columns.append({'id':'yield_rate','name':'yield_rate'})
    elif radio_value == 'thru_put':
        columns.append({'id':'thru_put','name':'thru_put'})
    
    return dff.to_dict('records'),columns


if __name__ == '__main__':
    app1.run(debug=True)