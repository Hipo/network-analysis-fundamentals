Networkx
========

Networkx is a Python library for analyzing and manipulating complex data networks. Its aim is to provide advanced functionality for grouping, moving and hierarchically organizing objects in a graph database.

A good example of a complex graph is a social network database that consists of links between a vast number of users and the objects they create on the network.

Basic Graph Terms
=================

There are a few network related terms that most programmers are already familiar with. Let's go over them to clarify:

Node (or Vertex)
----------------

This is the most basic element of a graph database. You can think of a node as the key in a dictionary. Under this key, we can store pieces of data, also called "Payloads". As an example, a user would be a node in a social network database.

Edge (Relationship)
-------------------

A relationship between two nodes is called an edge. Like nodes, edges can also store data and they can be either one-way or two-way links. A graph database that only has one-way relationships is called a "Directed Graph".

You can easily see examples of this in popular social networks. On Facebook, friendships are two-way edges, whereas on Twitter you are connected to people you follow with a one-way relationship.

Weight
------

Weight is a numerical value that determines relationship strength between two nodes. This could be used as distance, cost, or any other value. For instance on a computer network weight could mean the length of the cable connection between two computers.

Path
----

Path determines the series of nodes that should be traversed in order to get from one node to another. The most common graph problem is to determine the shortest path between two nodes.

In practice, this is used in a social network like LinkedIn to determine the people you need to get in touch with in order to connect with a user who is not in your network. Number of nodes in the shortest path determine the level of connection you have to that person.

Degree
------

Degree is the number of relationships that are connected to a node. With a specific group, the node with the highest number of connections can be called a "hub".


Let's Dive In
=============

Let's imagine social network where users can follow each other. We can put together a simple data model like the following:

```python
network = {
    "fatih": ["erdem", "mehmetbarancay", "tayyiperdogdu", "cemal",
              "taylan", "yigit", "serkan", "tuna", "cihanokyay"],
    "cemal": ["taylan", "yigit", "serkan", "sinan"],
    "erdem": ["fatih", "yigit"],
    "taylan": ["yigit", "serkan", "tuna", "cemal"],
    "yigit": ["yigit", "serkan", "tuna", "can"],
    "serkan": ["yigit", "serkan", "tuna", "erdem"],
    "tuna": ["yigit", "taylan", "can"],
    "can": ["yigit", "serkan", "fatih", "sinan"],
    "sinan": ["yigit", "serkan", "fatih", "cemal"],
    "suatavni": ["tayyiperdogdu", "abdullahcicek", "mehmetbarancay"],
    "tayyiperdogdu": ["abdullahcicek", "suatavni", "feyzullahgulen"],
    "abdullahcicek": ["feyzullahgulen"],
    "feyzullahgulen": ["suatavni", "tayyiperdogdu", "suatavni"],
    "mehmetbarancay": ["suatavni", "feyzullahgulen"],
    "cihanokyay": ["fatihkadirakin", "sametatdag", "gokmengorgen"],
    "fatihkadirakin": ["cihanokyay", "berkerpeksag", "johnresig"],
    "sametatdag": ["cihanokyay", "fatihkadirakin", "berkerpeksag"],
    "berkerpeksag": ["cihanokyay", "gokmengorgen"],
    "gokmengorgen": ["cihanokyay", "sametatdag", "berkerpeksag"],
    "eminbugrasakal": ["eminbugrasakal"],
    "johnresig": ["douglescrockford", "addyosmani", "marijnhaverbeke"],
    "addyosmani": ["douglescrockford", "johnresig", "marijnhaverbeke"],
    "trevorburnham": ["douglescrockford", "johnresig", "marijnhaverbeke"],
    "marijnhaverbeke": ["douglescrockford", "addyosmani", "trevorburnham"],
    "douglescrockford": ["martinfowler", "trevorburnham"],
    "martinfowler": ["douglescrockford", "johnresig"],
}
```

Dictionary keys are usernames and values are the list of people followed by that user. We can convert this to a graph that we can inspect with networks:

```python
import networkx as nx

# We are using a DirectedGraph here since the social network has one-way relationships
graph = nx.DiGraph()

# First thing to do is to add the nodes to the graph
graph.add_nodes_from(network.keys())
for users in network.values():
    for user in users:
        if not user in graph:
            graph.add_node(user)

# Then we determine the edges on the nodes
for user, followed_users in network.items():
    for followee in followed_users:
        graph.add_edge(user, followee)
```

Let's see how our graph looks:

```python
nx.draw(graph)
```

You can use the `matplotlib` library for converting the graph into a visual representation. Working with iPython Notebook, the output is drawn like this when you use `nx.draw`:

![graph](http://i.imgur.com/t8s0IUn.png "graph")

This is the graph output. Red circles are the nodes and the connections between them are the edges of the graph. Thicker relationship lines determine the directions of the edge.

When you inspect the graph, you will notice that some nodes are grouped together. You can think of these as local sub-groups on a social network. Nodes within these groups are closely tied to each other, and some nodes within them are also tied to other nodes in different groups.

Let's draw the nodes with their labels to get a better view:

![graph](http://i.imgur.com/K8n1ynn.png "graph")

The group at the bottom consists of the Python Istanbul members. Since they are all following each other, networkx automatically groups them together within the graph.

Now we can try to reach specific groups within this graph, these are also sometimes called "subgraphs". Networkx is capable of providing you with nodes that are not linked to any other node, or ones that are weakly or strongly connected within subgraphs.

We would like to fetch the strongly linked nodes:

```python
>>> list(nx.strongly_connected_components(graph))
	[['johnresig',
	  'marijnhaverbeke',
	  'addyosmani',
	  'trevorburnham',
	  'douglescrockford',
	  'martinfowler'],
	 ['fatihkadirakin',
	  'cihanokyay',
	  'sametatdag',
	  'berkerpeksag',
	  'gokmengorgen'],
	 ['mehmetbarancay',
	  'suatavni',
	  'tayyiperdogdu',
	  'abdullahcicek',
	  'feyzullahgulen'],
	 ['fatih',
	  'cemal',
	  'taylan',
	  'tuna',
	  'can',
	  'sinan',
	  'serkan',
	  'erdem',
	  'yigit']]
```

Networkx uses Tarjan's Algorithm to determine strong relationships, this is specifically effective in calculating connected nodes within a directed graph.

Now that we have our subgraphs, let's render each group with a different colour:

```python
subgraphs = list(nx.strongly_connected_components(graph))

# Name the colours with CSS colour names
colors = ["lightgreen", "lemonchiffon", "skyblue", "mistyrose", "aliceblue"]


def find_color(node):
	# Figure out the colour for each node
    for subgraph in subgraphs:
        if node in subgraph:
            return colors[subgraphs.index(subgraph)]

    # node bir gruba değil değil
    return "ghostwhite"

node_colors = map(find_color, graph.nodes())

# Render the final figure
plt.figure(figsize=(16, 10))
nx.draw(graph,
        with_labels=True,
        node_size=1400,
        node_color=node_colors,
        width=0.3)
```

And this is what we get:

![graph](http://i.imgur.com/DLMkXXV.png "graph")

Let's also name these:

	Blue: Politicians
	Pink: Hipo
	Yellow: Python İstanbul
	Green: JavaScripters

The rest if up to your imagination. As an example, we could try to figure out the list of people a person from Python Istanbul needs to get in touch with in order to reach someone from the Hipo group, or we could suggest similar people to follow to someone from the JavaScript group.

I recommend you read through the Networkx library's implementation to see the possibilities, there is a lot to discover.

Finally, you could also use an actual graph database like neo4j to solve similar problems. In practice, it's more common to dynamically calculate and scale specific paths and relationships.

- <http://networkx.github.io>
- <http://matplotlib.org>

Translation: <http://github.com/taylanpince>


