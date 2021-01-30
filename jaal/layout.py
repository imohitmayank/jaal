"""
Author: Mohit Mayank

Layout of the application
"""
# Import 
#---------
import visdcc
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
color_node = dbc.FormGroup([
                dbc.InputGroup([
                    dbc.InputGroupAddon("Color node by", addon_type="append"),
                    dbc.Select(
                        options=[
                            {"label": "Option 1", "value": 1},
                            {"label": "Option 2", "value": 2},
                        ]
                    ),]),
                dbc.FormText(
                "Select the categorical node property to color nodes by",
                color="secondary",
            ),])

# size node option
size_node = dbc.FormGroup([
                dbc.InputGroup([
                    dbc.InputGroupAddon("Size node by", addon_type="append"),
                    dbc.Select(
                        options=[
                            {"label": "Option 1", "value": 1},
                            {"label": "Option 2", "value": 2},
                        ]
                    ),]),
                dbc.FormText(
                "Select the numerical node property to size nodes by",
                color="secondary",
            ),])

# color edge option
color_edge = dbc.FormGroup([
                dbc.InputGroup([
                    dbc.InputGroupAddon("Color edge by", addon_type="append"),
                    dbc.Select(
                        options=[
                            {"label": "Option 1", "value": 1},
                            {"label": "Option 2", "value": 2},
                        ]
                    ),]),
                dbc.FormText(
                "Select the categorical edge property to color edge by",
                color="secondary",
            ),])

# size edge option
size_edge = dbc.FormGroup([
                dbc.InputGroup([
                    dbc.InputGroupAddon("Size edge by", addon_type="append"),
                    dbc.Select(
                        options=[
                            {"label": "Option 1", "value": 1},
                            {"label": "Option 2", "value": 2},
                        ]
                    ),]),
                dbc.FormText(
                "Select the numerical edge property to size edge by",
                color="secondary",
            ),])

def get_app_layout(graph_data):
    return html.Div([
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
                                data = graph_data,
                                options = dict(height= '600px', width= '100%'))
                ,width=9)]),
        ])
    