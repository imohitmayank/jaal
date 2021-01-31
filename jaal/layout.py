"""
Author: Mohit Mayank

Layout code for the application
"""
# Import 
#---------
import visdcc
import pandas as pd
import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc

# Constants
#--------------
# default node and egde color
DEFAULT_COLOR = '#97C2FC'

# Taken from https://stackoverflow.com/questions/470690/how-to-automatically-generate-n-distinct-colors
KELLY_COLORS_HEX = [
    "#FFB300", # Vivid Yellow
    "#803E75", # Strong Purple
    "#FF6800", # Vivid Orange
    "#A6BDD7", # Very Light Blue
    "#C10020", # Vivid Red
    "#CEA262", # Grayish Yellow
    "#817066", # Medium Gray

    # The following don't work well for people with defective color vision
    "#007D34", # Vivid Green
    "#F6768E", # Strong Purplish Pink
    "#00538A", # Strong Blue
    "#FF7A5C", # Strong Yellowish Pink
    "#53377A", # Strong Violet
    "#FF8E00", # Vivid Orange Yellow
    "#B32851", # Strong Purplish Red
    "#F4C800", # Vivid Greenish Yellow
    "#7F180D", # Strong Reddish Brown
    "#93AA00", # Vivid Yellowish Green
    "#593315", # Deep Yellowish Brown
    "#F13A13", # Vivid Reddish Orange
    "#232C16", # Dark Olive Green
    ]

# Code
#---------
def get_distinct_colors(n):
    """Return distict colors, currently atmost 20

    Parameters
    -----------
    n: int
        the distinct colors required
    """
    if n <= 20:
        return KELLY_COLORS_HEX[:n]

def create_card(id, value, description):
    """Creates card for high level stats

    Parameters
    ---------------
    """
    return dbc.Card(
        dbc.CardBody(
            [
                html.H4(id=id, children=value, className='card-title'),
                html.P(children=description),
            ]))

def fetch_row_style(style=""):
    return {'display': 'flex', 'flex-direction': 'row', 'justify-content': 'center', 'align-items': 'center'}

def create_row(children, style=""):
    return dbc.Row(children, 
                   style=fetch_row_style(style),
                   className="column flex-display")

search_form = dbc.FormGroup(
    [
        # dbc.Label("Search", html_for="search_graph"),
        dbc.Input(type="search", id="search_graph", placeholder="Search node in graph..."),
        dbc.FormText(
            "Highlight the node you are looking for.",
            color="secondary",
        ),
    ]
)

filter_node_form = dbc.FormGroup([
    # dbc.Label("Filter nodes", html_for="filter_nodes"),
    dbc.Textarea(id="filter_nodes", placeholder="Enter filter node query here..."),
    dbc.FormText(
        html.P([
            "Filter on nodes proprties by using ",
            html.A("Pandas Query syntax", 
            href="https://pandas.pydata.org/pandas-docs/stable/reference/api/pandas.DataFrame.query.html"),
        ]),
        color="secondary",
    ),
])

filter_edge_form = dbc.FormGroup([
    # dbc.Label("Filter edges", html_for="filter_edges"),
    dbc.Textarea(id="filter_edges", placeholder="Enter filter edge query here..."),
    dbc.FormText(
        html.P([
            "Filter on edges proprties by using ",
            html.A("Pandas Query syntax", 
            href="https://pandas.pydata.org/pandas-docs/stable/reference/api/pandas.DataFrame.query.html"),
        ]),
        color="secondary",
    ),
])

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

    Parameters
    --------------
    graph_data: dict{nodes, edges}
        network data in format of visdcc
    """
    # Step 1: find categorical features of nodes
    node_df = pd.DataFrame(graph_data['nodes'])
    cat_node_features = ['None'] + node_df.columns[(node_df.dtypes == 'object') & (node_df.apply(pd.Series.nunique) <= 20)].tolist()
    try: # remove irrelevant cols
        cat_node_features.remove('shape')
        cat_node_features.remove('label')
        cat_node_features.remove('id')
    except:
        pass
    # Step 2: find categorical features of edges
    edge_df = pd.DataFrame(graph_data['edges']).drop(columns=['color'])
    cat_edge_features = ['None'] + edge_df.columns[(edge_df.dtypes == 'object') & (edge_df.apply(pd.Series.nunique) <= 20)].tolist()
    try: # remove irrelevant cols
        cat_edge_features.remove('from')
        cat_edge_features.remove('to')
        cat_edge_features.remove('id')
    except:
        pass
    # Step 3: create and return the layout
    return html.Div([
            create_row(html.H2(children="Jaal")), # Title
            create_row([
                dbc.Col([
                    # setting panel
                    dbc.Form([
                        # html.H5("Setting Panel"),
                        # html.Hr(className="my-2"),
                        html.H6("Search"),
                        html.Hr(className="my-2"),
                        search_form, 
                        html.H6("Filter"),
                        html.Hr(className="my-2"),
                        filter_node_form, 
                        filter_edge_form,
                        html.H6("Color"),
                        html.Hr(className="my-2"), 
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
                            description='Select the categorical edge property to color edges by'
                        ), 
                    ], className="card", style={'padding': '5px', 'background': '#e5e5e5'}), 
                ],width=3, style={'display': 'flex', 'justify-content': 'center', 'align-items': 'center'}),
                # graph 
                dbc.Col(
                    visdcc.Network(id = 'graph', 
                                data = graph_data,
                                options = dict(height= '600px', width= '100%', interaction={'hover': True}))
                ,width=9)]),
            # stats cards
            # dbc.Row([
            #     dbc.Col(create_card(id="nodes_count", value="NA", description='Nodes'),width={'offset':3}),
            #     dbc.Col(create_card(id="edges_count", value="NA", description='Edges'),width={'offset':6})
            # ])
        ])
    