# import
from jaal import Jaal
from datasets.load_got import load_got
# load the data
edge_df, node_df = load_got()
# init Jaal and run server
Jaal(edge_df, node_df).plot(debug=True)
