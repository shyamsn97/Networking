import pyshark
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import networkx as nx
import seaborn as sns

#read in wireshark feed
cap = pyshark.FileCapture('test.pcap', only_summaries=True)
protocols = [cap.protocol for cap in cap]
destinations = [cap.destination for cap in cap]
sources = [cap.source for cap in cap]

df = pd.DataFrame({"sources":sources,"destinations":destinations,"protocols":protocols})
#We'll exclude arp commands
df = df.iloc[np.where(df["protocols"] != "ARP")]
graph = list(dict(zip(df["sources"],df["destinations"])).items())

def draw_graph(graph, labels=None,
               node_size=500, node_color='blue', node_alpha=0.3,
               node_text_size=8,
               edge_color='purple', edge_alpha=0.3, edge_tickness=1,
               edge_text_pos=0.2, edge_text_size = 1,
               text_font='sans-serif'):

    # create networkx graph
    G=nx.Graph()

    # edges
    for edge in graph:
        G.add_edge(edge[0], edge[1])

    graph_pos=nx.shell_layout(G,scale=2)

    # draw graph
    nx.draw_networkx_nodes(G,graph_pos,node_size=node_size, 
                           alpha=node_alpha, node_color=node_color)
    nx.draw_networkx_edges(G,graph_pos,width=edge_tickness,
                           alpha=edge_alpha,edge_color=edge_color)
    nx.draw_networkx_labels(G, graph_pos,font_size=node_text_size,
                            font_family=text_font)

    if labels is None:
        labels = range(len(graph))

    edge_labels = dict(zip(graph, labels))
    nx.draw_networkx_edge_labels(G, graph_pos, edge_labels=edge_labels, 
                                 label_pos=edge_text_pos)


plt.figure(figsize=(10,10))
plt.title('Network Graph')
draw_graph(graph,labels=df["protocols"])

plt.figure(figsize=(10,10))
plt.title('Protocol Type Frequency')
protocoltypes = list(set(protocols))
protocolfreq = [protocols.count(x) for x in protocoltypes]
protocolfreqdf = pd.DataFrame({'type':protocoltypes,"counts":protocolfreq})
sns.set_style("whitegrid")
sns.set(font_scale = 0.7)
ax = sns.barplot(x="type", y="counts", data=protocolfreqdf)
plt.show()
