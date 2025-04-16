import networkx as nx
from pyvis.network import Network

def build_relationship_graph(triples, output_html="relationship_graph.html"):
    G = nx.DiGraph()

    for subj, verb, obj in triples:
        G.add_node(subj, label=subj)
        G.add_node(obj, label=obj)
        G.add_edge(subj, obj, label=verb)

    try:
        net = Network(height="600px", width="100%", directed=True)
        net.from_nx(G)
        net.show(output_html)
    except Exception as e:
        print(f"❌ Failed to render graph: {e}")
        raise
    return output_html