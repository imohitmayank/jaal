"""
Author: Mohit Mayank

Parse network data from dataframe format into visdcc format 
"""


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
    if ("from" not in edge_df.columns) or ("to" not in edge_df.columns):
        raise Exception("Edge dataframe missing either 'from' or 'to' column.")
    # Check 2: if node_df is present, it should contain 'node' column
    if node_df is not None:
        if "id" not in node_df.columns:
            raise Exception("Node dataframe missing 'id' column.")

    # Data post processing - convert the from and to columns in edge data as string for searching
    edge_df.loc[:, ["from", "to"]] = edge_df.loc[:, ["from", "to"]].astype(str)

    # create node list w.r.t. the presence of absence of node_df
    nodes = []
    if node_df is None:
        node_list = list(
            set(edge_df["from"].unique().tolist() + edge_df["to"].unique().tolist())
        )
        nodes = [
            {"id": node_name, "label": node_name, "shape": "dot", "size": 7}
            for node_name in node_list
        ]
    else:
        # convert the node id column to string
        node_df.loc[:, "id"] = node_df.loc[:, "id"].astype(str)
        # create the node data
        for node in node_df.to_dict(orient="records"):
            nodes.append({**node, **{"label": node["id"], "shape": "dot", "size": 7}})

    # create edges from df
    edges = []
    for row in edge_df.to_dict(orient="records"):
        edges.append(
            {
                **row,
                **{"id": row["from"] + "__" + row["to"], "color": {"color": "#97C2FC"}},
            }
        )

    # return
    return {"nodes": nodes, "edges": edges}
