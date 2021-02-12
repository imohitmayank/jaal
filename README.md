<img src="jaal/assest/logo.png" alt="jaal logo"/>

[![PyPI version fury.io](https://badge.fury.io/py/ansicolortags.svg)](https://pypi.python.org/pypi/jaal/)

*Your interactive network visualizing dashboard*

Documentation: [Here](http://mohitmayank.com/jaal/)

## What is Jaal

Jaal is a python based interactive network visualizing tool built using Dash and Visdcc. Along with the basic features, Jaal also provides multiple option to play with the network data such as searching graph, filtering and even coloring nodes and edges in the graph. And all of this within 2 lines of codes :)

## Requirements

Jaal requires following python packages, 
1. Dash
    - dash_core_components
    - dash_html_components 
2. dash_bootstrap_components
3. visdcc
4. pandas

## Install

Installing Jaal is super easy, just do the following,

```bash
pip install jaal
```

And you are done :)

Note, it's recommended to create a virtual enivornment before installing. This can be easily done using `python -m venv myenv` and then to activate the env we need,
1. (Windows) `.\\myvenv\\Scripts\\activate.bat`
2. (Linux) `source myvenv/bin/activate`

## Getting started

After installing Jaal, we need to fetch the data and call `plot` function in Jaal. This can be shown by playing with an included Game of Thrones dataset, as follows,

```python
# import
from jaal import Jaal
from jaal.datasets import load_got
# load the data
edge_df, node_df = load_got()
# init Jaal and run server
Jaal(edge_df, node_df).plot()
```

Here first we import `Jaal` main class and the dataset loading function `load_got`. Later we load the GoT dataset from the datasets included in the package. This gives us two files,
1. **edge_df:** its a pandas dataframe with atleast `from` and `to` column, which represents the edge relationship between the entities
2. **node_df:** its an optional parameter, but should contains a `id` column with unique node names. 

Note, edge_df is mandatory and node_df is optional. Also we can include additional columns in these files which are automatically conidered as edge or node features respectively.

After running the plot, the console will prompt the default localhost address (`127.0.0.1:8050`) where Jaal is running. Access it to see the following dashboard,

<img src="jaal/assest/dashboard.png" alt="dashboard"/>

## Features

At present, the dashboard consist of following sections,
1. **Setting panel:** here we can play with the graph data, i further contain following sections, 
    - **Search:** can be used to highlight a node in graph
    - **Filter:** supports pandas query language and can be used to filter the graph data based on nodes or edge features.
    - **Color:** can be used to color nodes or edges based on their categorical features. Note, currently only features with at max 20 cardinality are supported. 
2. **Graph:** the network graph in all its glory :)

## Examples

### 1. Searching
<img src="jaal/assest/jaal_search.gif" alt="dashboard"/>

### 2. Filtering
<img src="jaal/assest/jaal_filter.gif" alt="dashboard"/>

### 3. Coloring
<img src="jaal/assest/jaal_color.gif" alt="dashboard"/>

## Issue tracker

Please report any bug or feature idea using Jaal issue tracker: https://github.com/imohitmayank/jaal/issues

## Collaboration

Any type of collaboration is appreciated. It could be  testing, development, documentation and other tasks that is useful to the project. Feel free to connect with me regarding this.

## Contact

You can connect with me on [LinkedIn](https://www.linkedin.com/in/imohitmayank/) or mail me at mohitmayank1@gmail.com.

## License

Jaal is licensed under the terms of the MIT License (see the file
LICENSE).
