from Bio import Phylo
from io import StringIO
import networkx as nx
import json
import matplotlib.pyplot as plt


def nexus_to_json_with_sequential_identifiers(nexus_content):
    handle = StringIO(nexus_content)
    tree = next(Phylo.parse(handle, 'nexus'))

    G = nx.DiGraph()
    unnamed_node_counter = 1  # Initialize a counter for unnamed nodes
    node_labels = {}  # To store node labels for drawing

    def add_clades(clade, parent=None):
        nonlocal unnamed_node_counter
        if clade.name:
            node_id = clade.name
        else:
            node_id = f"Node {unnamed_node_counter}"  # Assign a sequential identifier
            unnamed_node_counter += 1

        if parent:
            G.add_edge(parent, node_id, length=clade.branch_length if clade.branch_length else 0)
        node_labels[node_id] = node_id  # Add label for drawing

        for subclade in clade.clades:
            add_clades(subclade, node_id)

    add_clades(tree.clade)
    return nx.readwrite.json_graph.node_link_data(G), node_labels


# Sample Nexus content with possible unnamed nodes
nexus_data = """
#NEXUS
Begin taxa;
    Dimensions ntax=13;
    TaxLabels Equisetum_arvense Equisetum_fluviatile Equisetum_hyemale Equisetum_litorale Equisetum_moorei Equisetum_palustre Equisetum_pratense Equisetum_ramosissimum Equisetum_sylvaticum Equisetum_telmateia Equisetum_trachyodon Equisetum_variegatum Extinct_Sphenopsida;
End;

Begin trees;
    Translate
        1 Equisetum_arvense,
        2 Equisetum_fluviatile,
        3 Equisetum_hyemale,
        4 Equisetum_litorale,
        5 Equisetum_moorei,
        6 Equisetum_palustre,
        7 Equisetum_pratense,
        8 Equisetum_ramosissimum,
        9 Equisetum_sylvaticum,
        10 Equisetum_telmateia,
        11 Equisetum_trachyodon,
        12 Equisetum_variegatum,
        13 Extinct_Sphenopsida;
    tree 'PAUP_1' = [&U] (1:3,((((((2:2[trait:(12)12(12)1212?22(12)21?1?12(23)121211113],4:1):2,6:2):0,13:0):1,((((3:3,11:1):1,5:2):2,12:1):1,8:0):5):8,10:0):2,(7:1,9:1):2):0);
End;
"""

json_data, labels = nexus_to_json_with_sequential_identifiers(nexus_data)
# Convert the graph data for visualization
G = nx.readwrite.json_graph.node_link_graph(json_data)
print(json_data)
# Plotting the graph
pos = nx.spring_layout(G)  # Spring layout
nx.draw(G, pos, labels=labels, with_labels=True, node_color='lightblue', node_size=200, edge_color='gray')
plt.title('Phylogenetic Tree with Sequential Node Identifiers')
plt.axis('off')  # Turn off the axis
plt.show()
