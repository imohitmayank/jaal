"""
Author: Mohit Mayank

Main class for Jaal visualization
"""
# import
import dash
import visdcc
import pandas as pd
import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc
from dash.exceptions import PreventUpdate
from dash.dependencies import Input, Output, State
from datasets.parse_dataframe import parse_dataframe
from layout import get_app_layout, get_distinct_colors, DEFAULT_COLOR

# class
class Jaal:
    """
    """
    def __init__(self, edge_df, node_df=None):
        """
        Parameters
        -------------
        edge_df: pandas dataframe
            The network edge data stored in format of pandas dataframe 
    
        node_df: pandas dataframe (optional)
            The network node data stored in format of pandas dataframe 
        """
        print("Parsing the data...", end="")
        self.data = parse_dataframe(edge_df, node_df)
        self.filtered_data = self.data.copy()
        print("Done")

    def plot(self, debug=False):
        """Plot the network by running the Dash server 

        Parameter
        ----------
        debug: boolean
            run the debug instance of Dash?
        """
        # create the app
        app = dash.Dash(external_stylesheets=[dbc.themes.BOOTSTRAP])
        # # define layout
        app.layout = get_app_layout(self.data)
        # create the callbacks
        @app.callback(
            Output('graph', 'data'),
            [Input('search_graph', 'value'),
            Input('filter_nodes', 'value'),
            Input('filter_edges', 'value'),
            Input('color_nodes', 'value')],
            state=State('graph', 'data')
        )
        def setting_pane_callback(search_text, filter_nodes_text, filter_edges_text, color_nodes_value, graph_data):
            # fetch the id of option which triggered
            ctx = dash.callback_context
            if not ctx.triggered:
                print("No trigger")
                return PreventUpdate
            else:
                # find the id of the option which was triggered 
                input_id = ctx.triggered[0]['prop_id'].split('.')[0]
                # perform operation incase of search graph option
                if input_id == "search_graph":
                    # highlight the nodes which match the search text
                    nodes = graph_data['nodes']
                    for node in nodes:
                        if search_text not in node['label'].lower():
                            node['color'] = '#f4f8fe'
                        else:
                            node['color'] = DEFAULT_COLOR
                    graph_data['nodes'] = nodes
                # incase filter nodes was triggered
                elif input_id == 'filter_nodes':
                    print("inside filter with text:", filter_nodes_text)
                    self.filtered_data = self.data.copy()
                    node_df = pd.DataFrame(self.filtered_data['nodes'])
                    try:
                        node_list = node_df.query(filter_nodes_text)['id'].tolist()
                        nodes = []
                        for node in self.filtered_data['nodes']:
                            if node['id'] in node_list:
                                nodes.append(node)
                        self.filtered_data['nodes'] = nodes
                        graph_data = self.filtered_data
                    except: 
                        # node_list = node_df['id'].tolist()
                        graph_data = self.data
                        print("wrong node filter query!!")
                # incase filter edges was triggered
                elif input_id == 'filter_edges':
                    print("inside filter with text:", filter_edges_text)
                    self.filtered_data = self.data.copy()
                    edges_df = pd.DataFrame(self.filtered_data['edges'])
                    try:
                        edges_list = edges_df.query(filter_edges_text)['id'].tolist()
                        edges = []
                        for edge in self.filtered_data['edges']:
                            if edge['id'] in edges_list:
                                edges.append(edge)
                        self.filtered_data['edges'] = edges
                        graph_data = self.filtered_data
                    except:
                        # edges_list = edges_df['id'].tolist()
                        graph_data = self.data
                        print("wrong edge filter query!!")
                # If color option is selected
                if input_id == 'color_nodes':
                    # color option is None, revert back all changes
                    if color_nodes_value == 'None':
                        # revert to default color
                        for node in self.data['nodes']:
                            node['color'] = DEFAULT_COLOR
                    else:
                        print("inside color node", color_nodes_value)
                        unique_values = pd.DataFrame(self.data['nodes'])[color_nodes_value].unique()
                        colors = get_distinct_colors(len(unique_values))
                        value_color_mapping = {x:y for x, y in zip(unique_values, colors)}
                        for node in self.data['nodes']:
                            node['color'] = value_color_mapping[node[color_nodes_value]]
                        # import pdb; pdb.set_trace()
                    # filter the data currently shown
                    filtered_nodes = [x['id'] for x in self.filtered_data['nodes']]
                    # filtered_edges = [x['id'] for x in self.filtered_data['edges']]
                    self.filtered_data['nodes'] = [x for x in self.data['nodes'] if x['id'] in filtered_nodes]
                    graph_data = self.filtered_data
            # finally return the modified data
            return graph_data
        # run the server
        app.run_server(debug=debug)

# Testing main call
if __name__ == "__main__":
    # import
    from datasets.load_got import load_got
    # load the data
    edge_df, node_df = load_got()
    # init Jaal and run server
    Jaal(edge_df, node_df).plot(debug=True)
