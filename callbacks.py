# """
# Author: Mohit Mayank

# Specify all callbacks of the app 
# """

# # Import
# import dash
# from dash.exceptions import PreventUpdate
# from dash.dependencies import Input, Output, State

# # Callbacks
# @app.callback(
#     Output('graph', 'data'),
#     [Input('search_graph', 'value'),
#      Input('filter_nodes', 'value')],
#     state=State('graph', 'data')
# )
# def setting_pane_callback(search_text, filter_nodes_text, graph_data):
#     # fetch the id of option which triggered
#     ctx = dash.callback_context
#     if not ctx.triggered:
#         print("No trigger")
#         return PreventUpdate
#     else:
#         input_id = ctx.triggered[0]['prop_id'].split('.')[0]
#         print(input_id)
#         # perform operation incase of search graph option
#         # if input_id == "search_graph":

#     # highlight the nodes which match the search text
#     nodes = graph_data['nodes']
#     for node in nodes:
#         if search_text not in node['label'].lower():
#             node['color'] = '#f4f8fe'
#             # node['hidden'] = True
#         else:
#             node['color'] = '#97C2FC'
#             # node['hidden'] = False
#     graph_data['nodes'] = nodes
#     return graph_data