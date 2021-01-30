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
from generic_layout import *
from callbacks import *
from dash.dependencies import Input, Output, State

# create app
app = dash.Dash(external_stylesheets=[dbc.themes.BOOTSTRAP])

# load data
df = pd.read_csv("data/book1.csv")
df = df.loc[df['weight']>10, :]
node_list = list(set(df['Source'].unique().tolist() + df['Target'].unique().tolist()))
nodes = [{'id': node_name, 'label': node_name, 'shape': 'dot', 'size': 7, 'opacity': 10} for i, node_name in enumerate(node_list)]
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
    create_row(html.H2(children="Jaal")), # Title
    # divide cols for rest components
    dbc.Row([
        dbc.Col([
            dbc.Form([search_form, filter_node_form, filter_edge_form, color_node, size_node, color_edge, size_edge]), # setting panel
            # dcc.RadioItems(id = 'color',
            #             options=[{'label': 'Red'  , 'value': '#ff0000'},
            #                     {'label': 'Green', 'value': '#00ff00'},
            #                     {'label': 'Blue' , 'value': '#0000ff'} ],
            #             value='Red')             ,
        ]
        ,width=3),
        
        dbc.Col(
            visdcc.Network(id = 'graph', 
                        data = {'nodes': nodes, 'edges': edges},
                        options = dict(height= '600px', width= '100%'))
        ,width=9)]),
])

# define callback
# @app.callback(
#     Output('net', 'options'),
#     [Input('color', 'value')])
# def myfun(x):
#     return {'nodes':{'color': x}}

@app.callback(
    Output('graph', 'data'),
    [Input('search_graph', 'value')],
    state=State('graph', 'data')
)
def search_option_callback(search_text, graph_data):
    # highlight the nodes which match the search text
    nodes = graph_data['nodes']
    for node in nodes:
        if search_text not in node['label'].lower():
            node['color'] = '#f4f8fe'
            # node['hidden'] = True
        else:
            node['color'] = '#97C2FC'
            # node['hidden'] = False
    graph_data['nodes'] = nodes
    return graph_data

# define main calling
if __name__ == '__main__':
    app.run_server(debug=True)
