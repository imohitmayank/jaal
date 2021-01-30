"""
Author: Mohit Mayank

Layout of the application
"""
# Import 
#---------
import visdcc
import pandas as pd
import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc

# Code
#---------
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

# list of common styles of row alignment
def fetch_row_style(style=""):
    return {'display': 'flex', 'flex-direction': 'row', 'justify-content': 'center', 'align-items': 'center'}

def create_row(children, style=""):
    return dbc.Row(children, 
                   style=fetch_row_style(style),
                   className="column flex-display")

search_form = dbc.FormGroup(
    [
        dbc.Label("Search", html_for="search_graph"),
        dbc.Input(type="search", id="search_graph", placeholder="Search node in graph..."),
        dbc.FormText(
            "Find the node you are looking for.",
            color="secondary",
        ),
    ]
)

filter_node_form = dbc.FormGroup([
    dbc.Label("Filter nodes", html_for="filter_nodes"),
    dbc.Textarea(id="filter_nodes", placeholder="Enter filter node query here..."),
    dbc.FormText(
        "Filter on nodes properties by using Pandas Query syntax",
        color="secondary",
    ),
])

filter_edge_form = dbc.FormGroup([
    dbc.Label("Filter edges", html_for="filter_edges"),
    dbc.Textarea(id="filter_edges", placeholder="Enter filter edge query here..."),
    dbc.FormText(
        "Filter on edge proprties by using Pandas Query syntax",
        color="secondary",
    ),
])

# color node option
# color_node = dbc.FormGroup([
#                 dbc.InputGroup([
#                     dbc.InputGroupAddon("Color node by", addon_type="append"),
#                     dbc.Select(
#                         id="color_nodes",
#                         options=[
#                             {"label": "Option 1", "value": 1},
#                             {"label": "Option 2", "value": 2},
#                         ]
#                     ),]),
#                 dbc.FormText(
#                 "Select the categorical node property to color nodes by",
#                 color="secondary",
#             ),])

# size node option
# size_node = dbc.FormGroup([
#                 dbc.InputGroup([
#                     dbc.InputGroupAddon("Size node by", addon_type="append"),
#                     dbc.Select(
#                         options=[
#                             {"label": "Option 1", "value": 1},
#                             {"label": "Option 2", "value": 2},
#                         ]
#                     ),]),
#                 dbc.FormText(
#                 "Select the numerical node property to size nodes by",
#                 color="secondary",
#             ),])

# color edge option
# color_edge = dbc.FormGroup([
#                 dbc.InputGroup([
#                     dbc.InputGroupAddon("Color edge by", addon_type="append"),
#                     dbc.Select(
#                         options=[
#                             {"label": "Option 1", "value": 1},
#                             {"label": "Option 2", "value": 2},
#                         ]
#                     ),]),
#                 dbc.FormText(
#                 "Select the categorical edge property to color edge by",
#                 color="secondary",
#             ),])

# size edge option
# size_edge = dbc.FormGroup([
#                 dbc.InputGroup([
#                     dbc.InputGroupAddon("Size edge by", addon_type="append"),
#                     dbc.Select(
#                         options=[
#                             {"label": "Option 1", "value": 1},
#                             {"label": "Option 2", "value": 2},
#                         ]
#                     ),]),
#                 dbc.FormText(
#                 "Select the numerical edge property to size edge by",
#                 color="secondary",
#             ),])

def get_select_form_layout(id, options, label, description):
    """Creates a select (dropdown) form with provides details

    Parameters
    -----------
    id: str
        id of the form
    options: list
        options to show
    label: str
        label of the select dropdown bar
    description: str
        long text detail of the setting
    """
    return  dbc.FormGroup([
                dbc.InputGroup([
                    dbc.InputGroupAddon(label, addon_type="append"),
                    dbc.Select(id=id,
                        options=options
                    ),]),
                dbc.FormText(description, color="secondary",)
            ,])

def get_app_layout(graph_data):
    """Create and return the layout of the app
    """
    # find categorical features of nodes
    node_df = pd.DataFrame(graph_data['nodes'])
    cat_node_features = node_df.columns[node_df.dtypes == 'object'].tolist() 
    cat_node_features.remove('id')
    cat_node_features.remove('label')
    cat_node_features.remove('shape')
    # find categorical features of edges
    edge_df = pd.DataFrame(graph_data['edges'])
    cat_edge_features = edge_df.columns[edge_df.dtypes == 'object'].tolist() 
    cat_edge_features.remove('from')
    cat_edge_features.remove('to')
    cat_edge_features.remove('id')
    # return the layout
    return html.Div([
            create_row(html.H2(children="Jaal")), # Title
            dbc.Row([
                dbc.Col([
                    # setting panel
                    dbc.Form([search_form, 
                             filter_node_form, 
                             filter_edge_form, 
                             get_select_form_layout(
                                 id='color_nodes',
                                 options=[{'label': opt, 'value': opt} for opt in cat_node_features],
                                 label='Color nodes by',
                                 description='Select the categorical node property to color nodes by'
                             ), 
                             get_select_form_layout(
                                 id='color_edges',
                                 options=[{'label': opt, 'value': opt} for opt in cat_edge_features],
                                 label='Color edges by',
                                 description='Select the categorical edges property to color nodes by'
                             ), 
                             ]), 
                ]
                ,width=3),
                
                dbc.Col(
                    visdcc.Network(id = 'graph', 
                                data = graph_data,
                                options = dict(height= '600px', width= '100%'))
                ,width=9)]),
        ])
    