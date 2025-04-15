import networkx as nx
from pyvis.network import Network

def build_relationship_graph(triples, output_html="relationship_graph.html"):
    G = nx.DiGraph()

    for subj, verb, obj in triples:
        G.add_node(subj, label=subj)
        G.add_node(obj, label=obj)
        G.add_edge(subj, obj, label=verb)

    net = Network(height="600px", width="100%", directed=True)
    net.from_nx(G)
    net.show(output_html)

    return output_html