"""
Author: Mohit Mayank

Main class for Jaal network visualization dashboard
"""
# import
import dash
import visdcc
import pandas as pd
from dash import dcc, html
# import dash_core_components as dcc
# import dash_html_components as html
import dash_bootstrap_components as dbc
from dash.exceptions import PreventUpdate
from dash.dependencies import Input, Output, State
from .datasets.parse_dataframe import parse_dataframe
from .layout import get_app_layout, get_distinct_colors, create_color_legend, DEFAULT_COLOR, DEFAULT_NODE_SIZE, DEFAULT_EDGE_SIZE

# class
class Jaal:
    """The main visualization class
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
        self.data, self.scaling_vars = parse_dataframe(edge_df, node_df)
        self.filtered_data = self.data.copy()
        self.node_value_color_mapping = {}
        self.edge_value_color_mapping = {}
        print("Done")

    def _callback_search_graph(self, graph_data, search_text):
        """Only show the nodes which match the search text
        """
        nodes = graph_data['nodes']
        for node in nodes:
            if search_text not in node['label'].lower():
                node['hidden'] = True
            else:
                node['hidden'] = False
        graph_data['nodes'] = nodes
        return graph_data

    def _callback_filter_nodes(self, graph_data, filter_nodes_text):
        """Filter the nodes based on the Python query syntax
        """
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
            graph_data = self.data
            print("wrong node filter query!!")
        return graph_data

    def _callback_filter_edges(self, graph_data, filter_edges_text):
        """Filter the edges based on the Python query syntax
        """
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
            graph_data = self.data
            print("wrong edge filter query!!")
        return graph_data

    def _callback_color_nodes(self, graph_data, color_nodes_value):
        value_color_mapping = {}
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
        # filter the data currently shown
        filtered_nodes = [x['id'] for x in self.filtered_data['nodes']]
        self.filtered_data['nodes'] = [x for x in self.data['nodes'] if x['id'] in filtered_nodes]
        graph_data = self.filtered_data
        return graph_data, value_color_mapping
    
    def _callback_size_nodes(self, graph_data, size_nodes_value):

        # color option is None, revert back all changes
        if size_nodes_value == 'None':
            # revert to default color
            for node in self.data['nodes']:
                node['size'] = DEFAULT_NODE_SIZE
        else:
            print("Modifying node size using ", size_nodes_value)
            # fetch the scaling value
            minn = self.scaling_vars['node'][size_nodes_value]['min']
            maxx = self.scaling_vars['node'][size_nodes_value]['max']
            # define the scaling function
            scale_val = lambda x: 20*(x-minn)/(maxx-minn)
            # set size after scaling
            for node in self.data['nodes']:
                node['size'] = node['size'] + scale_val(node[size_nodes_value])
        # filter the data currently shown
        filtered_nodes = [x['id'] for x in self.filtered_data['nodes']]
        self.filtered_data['nodes'] = [x for x in self.data['nodes'] if x['id'] in filtered_nodes]
        graph_data = self.filtered_data
        return graph_data

    def _callback_color_edges(self, graph_data, color_edges_value):
        value_color_mapping = {}
        # color option is None, revert back all changes
        if color_edges_value == 'None':
            # revert to default color
            for edge in self.data['edges']:
                edge['color']['color'] = DEFAULT_COLOR
        else:
            print("inside color edge", color_edges_value)
            unique_values = pd.DataFrame(self.data['edges'])[color_edges_value].unique()
            colors = get_distinct_colors(len(unique_values))
            value_color_mapping = {x:y for x, y in zip(unique_values, colors)}
            for edge in self.data['edges']:
                edge['color']['color'] = value_color_mapping[edge[color_edges_value]]
        # filter the data currently shown
        filtered_edges = [x['id'] for x in self.filtered_data['edges']]
        self.filtered_data['edges'] = [x for x in self.data['edges'] if x['id'] in filtered_edges]
        graph_data = self.filtered_data
        return graph_data, value_color_mapping

    def _callback_size_edges(self, graph_data, size_edges_value):
        # color option is None, revert back all changes
        if size_edges_value == 'None':
            # revert to default color
            for edge in self.data['edges']:
                edge['width'] = DEFAULT_EDGE_SIZE
        else:
            print("Modifying edge size using ", size_edges_value)
            # fetch the scaling value
            minn = self.scaling_vars['edge'][size_edges_value]['min']
            maxx = self.scaling_vars['edge'][size_edges_value]['max']
            # define the scaling function
            scale_val = lambda x: 20*(x-minn)/(maxx-minn)
            # set the size after scaling
            for edge in self.data['edges']:
                edge['width'] = scale_val(edge[size_edges_value])
        # filter the data currently shown
        filtered_edges = [x['id'] for x in self.filtered_data['edges']]
        self.filtered_data['edges'] = [x for x in self.data['edges'] if x['id'] in filtered_edges]
        graph_data = self.filtered_data
        return graph_data

    def get_color_popover_legend_children(self, node_value_color_mapping={}, edge_value_color_mapping={}):
        """Get the popover legends for node and edge based on the color setting
        """
        # var
        popover_legend_children = []

        # common function
        def create_legends_for(title="Node", legends={}):
            # add title
            _popover_legend_children = [dbc.PopoverHeader(f"{title} legends")]
            # add values if present
            if len(legends) > 0:
                for key, value in legends.items():
                    _popover_legend_children.append(
                        # dbc.PopoverBody(f"Key: {key}, Value: {value}")
                        create_color_legend(key, value)
                        )
            else: # otherwise add filler
                _popover_legend_children.append(dbc.PopoverBody(f"no {title.lower()} colored!"))
            #
            return _popover_legend_children

        # add node color legends
        popover_legend_children.extend(create_legends_for("Node", node_value_color_mapping))
        # add edge color legends
        popover_legend_children.extend(create_legends_for("Edge", edge_value_color_mapping))
        #
        return popover_legend_children

    def create(self, directed=False, vis_opts=None):
        """Create the Jaal app and return it

        Parameter
        ----------
            directed: boolean
                process the graph as directed graph?

            vis_opts: dict
                the visual options to be passed to the dash server (default: None)

        Returns
        -------
            app: dash.Dash
                the Jaal app
        """
        # create the app
        app = dash.Dash(external_stylesheets=[dbc.themes.BOOTSTRAP])

        # define layout
        app.layout = get_app_layout(self.data, color_legends=self.get_color_popover_legend_children(), directed=directed, vis_opts=vis_opts)

        # create callbacks to toggle legend popover
        @app.callback(
            Output("color-legend-popup", "is_open"),
            [Input("color-legend-toggle", "n_clicks")],
            [State("color-legend-popup", "is_open")],
        )
        def toggle_popover(n, is_open):
            if n:
                return not is_open
            return is_open

        # create callbacks to toggle hide/show sections - FILTER section
        @app.callback(
            Output("filter-show-toggle", "is_open"),
            [Input("filter-show-toggle-button", "n_clicks")],
            [State("filter-show-toggle", "is_open")],
        )
        def toggle_filter_collapse(n, is_open):
            if n:
                return not is_open
            return is_open
        
        # create callbacks to toggle hide/show sections - COLOR section
        @app.callback(
            Output("color-show-toggle", "is_open"),
            [Input("color-show-toggle-button", "n_clicks")],
            [State("color-show-toggle", "is_open")],
        )
        def toggle_filter_collapse(n, is_open):
            if n:
                return not is_open
            return is_open

        # create callbacks to toggle hide/show sections - COLOR section
        @app.callback(
            Output("size-show-toggle", "is_open"),
            [Input("size-show-toggle-button", "n_clicks")],
            [State("size-show-toggle", "is_open")],
        )
        def toggle_filter_collapse(n, is_open):
            if n:
                return not is_open
            return is_open

        # create the main callbacks
        @app.callback(
            [Output('graph', 'data'), Output('color-legend-popup', 'children')],
            [Input('search_graph', 'value'),
            Input('filter_nodes', 'value'),
            Input('filter_edges', 'value'),
            Input('color_nodes', 'value'),
            Input('color_edges', 'value'),
            Input('size_nodes', 'value'),
            Input('size_edges', 'value')],
            [State('graph', 'data')]
        )
        def setting_pane_callback(search_text, filter_nodes_text, filter_edges_text, 
                    color_nodes_value, color_edges_value, size_nodes_value, size_edges_value, graph_data):
            # fetch the id of option which triggered
            ctx = dash.callback_context
            # if its the first call
            if not ctx.triggered:
                print("No trigger")
                return [self.data, self.get_color_popover_legend_children()]
            else:
                # find the id of the option which was triggered
                input_id = ctx.triggered[0]['prop_id'].split('.')[0]
                # perform operation in case of search graph option
                if input_id == "search_graph":
                    graph_data = self._callback_search_graph(graph_data, search_text)
                # In case filter nodes was triggered
                elif input_id == 'filter_nodes':
                    graph_data = self._callback_filter_nodes(graph_data, filter_nodes_text)
                # In case filter edges was triggered
                elif input_id == 'filter_edges':
                    graph_data = self._callback_filter_edges(graph_data, filter_edges_text)
                # If color node text is provided
                if input_id == 'color_nodes':
                    graph_data, self.node_value_color_mapping = self._callback_color_nodes(graph_data, color_nodes_value)
                # If color edge text is provided
                if input_id == 'color_edges':
                    graph_data, self.edge_value_color_mapping = self._callback_color_edges(graph_data, color_edges_value)
                # If size node text is provided
                if input_id == 'size_nodes':
                    graph_data = self._callback_size_nodes(graph_data, size_nodes_value)
                # If size edge text is provided
                if input_id == 'size_edges':
                    graph_data = self._callback_size_edges(graph_data, size_edges_value)
            # create the color legend childrens
            color_popover_legend_children = self.get_color_popover_legend_children(self.node_value_color_mapping, self.edge_value_color_mapping)
            # finally return the modified data
            return [graph_data, color_popover_legend_children]
        # return server
        return app

    def plot(self, debug=False, host="127.0.0.1", port="8050", directed=False, vis_opts=None):
        """Plot the Jaal by first creating the app and then hosting it on default server

        Parameter
        ----------
            debug (boolean)
                run the debug instance of Dash?

            host: string
                ip address on which to run the dash server (default: 127.0.0.1)

            port: string
                port on which to expose the dash server (default: 8050)

            directed (boolean):
                whether the graph is directed or not (default: False)

            vis_opts: dict
                the visual options to be passed to the dash server (default: None)
        """
        # call the create_graph function
        app = self.create(directed=directed, vis_opts=vis_opts)
        # run the server
        app.run_server(debug=debug, host=host, port=port)