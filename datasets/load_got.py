"""
Author: Mohit Mayank

Load and return the Game of Thrones dataset

Data details:
1. 
"""

# imports
import pandas as pd

# data load and return function
def load_got(filter_conections_threshold=10):
    """Load the first book of the Got Dataset

    Parameters
    -----------
    filter_conections_threshold: int
        keep the connections in GoT dataset with weights greater than this threshold 
    """
    # load the edge and node data
    edge_df = pd.read_csv("datasets/got/got_edge_df.csv")
    node_df = pd.read_csv("datasets/got/got_node_df.csv")
    # return 
    return edge_df, node_df