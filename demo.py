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

from matplotlib import pyplot as plt
import networkx as nx


# sosyal ağımız tek yönlü ilişkilerden oluşmaktadır.
# bu sebeple DirectedGraph kullanmalıyız.
graph = nx.DiGraph()

# ilk yapmamız gereken oluşturduğumuz graph'a nodları eklemek
graph.add_nodes_from(network.keys())
for users in network.values():
    for user in users:
        if not user in graph:
            graph.add_node(user)

# node'lar üzerindeki ilişkileri (edge) tanımlıyoruz
for user, followed_users in network.items():
    for followee in followed_users:
        graph.add_edge(user, followee)

subgraphs = list(nx.strongly_connected_components(graph))

# html isimleri ile renklerimizi tanımlıyoruz
colors = ["lightgreen", "lemonchiffon", "skyblue", "mistyrose", "aliceblue"]


def find_color(node):
    # node'un dahil olduğu grup üzerinden rengini buluyoruz
    for subgraph in subgraphs:
        if node in subgraph:
            return colors[subgraphs.index(subgraph)]

    # node bir gruba değil değil
    return "ghostwhite"

node_colors = map(find_color, graph.nodes())

# çıktımızın görsel değerlerini belirleyip render ettiriyoruz
plt.figure(figsize=(16, 10))
nx.draw(graph,
        with_labels=True,
        node_size=1400,
        node_color=node_colors,
        width=0.3)
