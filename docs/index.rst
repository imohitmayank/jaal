.. jaal documentation master file, created by
   sphinx-quickstart on Tue Feb  9 21:43:05 2021.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

Introducing Jaal - Interacting with Network Made Easy!
================================================================

|PyPI version shields.io|

.. |PyPI version shields.io| image:: https://img.shields.io/pypi/v/jaal.svg
   :target: hhttps://img.shields.io/pypi/v/jaal

|PyPI download month|

.. |PyPI download month| image:: https://img.shields.io/pypi/dm/jaal.svg
   :target:  https://img.shields.io/pypi/v/jaal.svg
   
Your interactive network visualizing dashboard in Python

Visit the package's `github page <https://github.com/imohitmayank/jaal/>`_ , and if you like it, please don't shy from clicking on the star 😏

---

👉 What is Jaal?
-----------------
Jaal is a python based interactive network visualizing tool built using Dash and Visdcc. As it's built using Dash, we can consider it as more of a dashboard rather than a network plot. Because of this, along with the basic features, Jaal also provides multiple options to play with the network data such as searching, filtering and even colouring nodes and edges in the graph. And all of this within 2 lines of codes :)

👉 Install
--------------
Installing Jaal is super easy, just run the following,  ::

   pip install jaal

And you are done 😆

Note, it's recommended to create a virtual environment before installing. This can be easily done using python -m venv myenv and then to activate the environment we run,

1. (Windows) ``.\\myvenv\\Scripts\\activate.bat``

2. (Linux) ``source myvenv/bin/activate``

👉 Getting started
--------------------
After installing Jaal, we need to fetch the data and call plot function in Jaal. Let's do this by playing with Game of Thrones dataset which is included in the package. The complete code to fetch the data and plot is as follows, ::

   # import
   from jaal import Jaal
   from jaal.datasets import load_got
   # load the data
   edge_df, node_df = load_got()
   # init Jaal and run server
   Jaal(edge_df, node_df).plot()

Here first we import Jaal main class and the dataset loading function load_got. Later we loaded the GoT dataset from the package. This gives us two files,

1. **edge_df:** it's a pandas dataframe with at least from and to columns, which represents the edge relationship between the entities

2. **node_df:** it's a pandas dataframe with at least id column which contains the unique node names

Note, edge_df is mandatory and node_df is optional. Also, we can include additional columns in these files which are automatically considered as edge or node features respectively.

Next, we pass the data into Jaal and call plot. This will lead the console to prompt the default localhost address (127:0.0.1:8050) where Jaal is running. We can access it to see the following dashboard,

.. figure::  source/dashboard.png
   :align:   center

   Jaal Dashboard

👉 Features
--------------

At present, the dashboard consist of the following sections,

1. **Settings panel:** here we have multiple options to play with the graph data. It further contains the following sub-sections,
   
   a. **Search:** can be used to highlight a node in the graph
   
   b. **Filter:** supports pandas query language and can be used to filter the graph data based on nodes or edge features.
   
   c. **Color:** can be used to color nodes or edges based on their categorical features. Note, currently only features with at max 20 cardinality are supported.

2. **Graph:** the network graph plotted using visdcc.

👉 Examples
---------------

Let's go through the example of each of the features we discussed above one by one. We will use the GoT dataset.

1. **Searching**

The first option is searching, where we can search for a specific node in the graph. It supports character by character search on the node labels. Below is an example where we are trying to search for "Arya",

.. figure::  source/jaal_search.gif
   :align:   center

2. **Filtering**

Next, we have filtering. Jaal supports the option to search on both node and edges features. For this, we provide separate text areas. Below we can see the live effect of node and edge filtering query.

.. figure::  source/jaal_filter.gif
   :align:   center

3. **Coloring**

Finally, instead of filtering, we may want to see the overall distribution of any feature. Currently, Jaal handles this by providing the option to color nodes or edges based on any categorical feature. We can see a live-action example below.

.. figure::  source/jaal_color.gif
   :align:   center

---------------


.. toctree::
   :maxdepth: 2

   code

.. toctree::
   :maxdepth: 2

   changelog

   
Indices and tables
--------------------

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`

---------------

Connect with me on `LinkedIn <https://www.linkedin.com/in/imohitmayank/>`_ .