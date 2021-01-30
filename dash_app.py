"""
Author: Mohit Mayank

Dash application using visdcc for network visualization UI.
"""
# imports
import dash
import visdcc
import pandas as pd
import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc
from generic_layout import create_row
from dash.dependencies import Input, Output, State

# create app
app = dash.Dash()

# load data
df = pd.read_csv("data/book1.csv")
df = df.loc[df['weight']>10, :]
node_list = list(set(df['Source'].unique().tolist() + df['Target'].unique().tolist()))
nodes = [{'id': node_name, 'label': node_name, 'shape': 'dot', 'size': 7} for i, node_name in enumerate(node_list)]
# create edges from df
edges = []
for row in df.to_dict(orient='records'):
    source, target = row['Source'], row['Target']
    edges.append({
        'id': source + "__" + target,
        'from': source,
        'to': target,
        'width': 2,
    })

# helper functions
def create_card(id, title, value, description=""):
    return dbc.Card(
        dbc.CardBody(
            [
                html.H4(title),
                html.P(id=id, children=value),
                html.H6(description)
            ]
        )
    )

# define layout
app.layout = html.Div([
    # Title
    create_row(html.H2(children="Jaal")),
    create_row(
        visdcc.Network(id = 'net', 
                    data = {'nodes': nodes, 'edges': edges},
                    options = dict(height= '600px', width= '100%'))
    ),
    create_row(
        dcc.RadioItems(id = 'color',
                    options=[{'label': 'Red'  , 'value': '#ff0000'},
                            {'label': 'Green', 'value': '#00ff00'},
                            {'label': 'Blue' , 'value': '#0000ff'} ],
                    value='Red')             
    )
])

# define callback
@app.callback(
    Output('net', 'options'),
    [Input('color', 'value')])
def myfun(x):
    return {'nodes':{'color': x}}

# define main calling
if __name__ == '__main__':
    app.run_server(debug=True)
