"""
Author: Mohit Mayank

Parse network data from dataframe format into visdcc format 
"""

def compute_scaling_vars_for_numerical_cols(df):
    """Identify and scale numerical cols"""
    # identify numerical cols
    numerics = ['int16', 'int32', 'int64', 'float16', 'float32', 'float64']
    numeric_cols = df.select_dtypes(include=numerics).columns.tolist()
    # var to hold the scaling function
    scaling_vars = {}
    # scale numerical cols
    for col in numeric_cols:
        minn, maxx = df[col].min(), df[col].max()
        scaling_vars[col] = {'min': minn, 'max': maxx} 
    # return
    return scaling_vars

def parse_dataframe(edge_df, node_df=None):
    """Parse the network dataframe into visdcc format

    Parameters
    -------------
    edge_df: pandas dataframe
            The network edge data stored in format of pandas dataframe 
    
    node_df: pandas dataframe (optional)
            The network node data stored in format of pandas dataframe 
    """
    # Data checks
    # Check 1: mandatory columns presence
    if ('from' not in edge_df.columns) or ('to' not in edge_df.columns):
        raise Exception("Edge dataframe missing either 'from' or 'to' column.")
    # Check 2: if node_df is present, it should contain 'node' column
    if node_df is not None:
        if 'id' not in node_df.columns:
            raise Exception("Node dataframe missing 'id' column.")

    # Data post processing - convert the from and to columns in edge data as string for searching
    edge_df.loc[:, ['from', 'to']] = edge_df.loc[:, ['from', 'to']].astype(str)

    # Data pot processing (scaling numerical cols in nodes and edge)
    scaling_vars = {'node': None, 'edge': None}
    if node_df is not None:
        scaling_vars['node'] = compute_scaling_vars_for_numerical_cols(node_df)
    scaling_vars['edge'] = compute_scaling_vars_for_numerical_cols(edge_df)
    
    # create node list w.r.t. the presence of absence of node_df
    nodes = []
    if node_df is None:
        node_list = list(set(edge_df['from'].unique().tolist() + edge_df['to'].unique().tolist()))
        nodes = [{'id': node_name, 'label': node_name, 'title': node_name, 'shape': 'dot', 'size': 7} for node_name in node_list]
    else:
        # convert the node id column to string
        node_df.loc[:, 'id'] = node_df.loc[:, 'id'].astype(str)
        # remove blanks cols
        node_df = node_df.dropna(axis=1)
        # if title is not present, make it same as label
        if 'title' not in node_df.columns:
            node_df['title'] = node_df['id']
        # see if node imge url is present or not
        node_image_url_flag = 'node_image_url' in node_df.columns
        # create the node data
        for node in node_df.to_dict(orient='records'):
            if not node_image_url_flag:
                nodes.append({**node, **{'label': node['id'], 'shape': 'dot', 'size': 7}})
            else:
                nodes.append({**node, **{'label': node['id'], 'shape': 'circularImage',
                                'image': node['node_image_url'], 
                                'size': 20}})

    # create edges from df
    edges = []
    for row in edge_df.to_dict(orient='records'):
        edges.append({**row, **{'id': row['from'] + "__" + row['to'],  'color': {'color': '#97C2FC'}}})
    
    # return
    return {'nodes': nodes, 'edges': edges}, scaling_vars