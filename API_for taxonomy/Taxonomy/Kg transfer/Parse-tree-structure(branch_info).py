from Bio import Phylo
from io import StringIO
import json
import uuid
import networkx as nx
import matplotlib.pyplot as plt

def nexus_to_json_with_traits_on_edges(nexus_content):
    handle = StringIO(nexus_content)
    tree = next(Phylo.parse(handle, 'nexus'))

    graph = {'nodes': [], 'edges': []}

    def parse_clade(clade, parent_id=None):
        node_id = str(uuid.uuid4())
        node_label = clade.name if clade.name else node_id

        graph['nodes'].append({'id': node_id, 'label': node_label})

        if parent_id:
            # Initialize traits and states as empty strings
            traits = ''
            states = ''
            # Check if comment is present and extract traits or states if available
            if clade.comment:
                comment_parts = clade.comment.replace('[&', '').replace(']', '').split(',')
                for part in comment_parts:
                    if 'traits=' in part:
                        traits = part.split('=')[1]
                    elif 'states=' in part:
                        states = part.split('=')[1]
            branch_length = clade.branch_length if clade.branch_length else 0
            graph['edges'].append({
                'source': parent_id,
                'target': node_id,
                'length': branch_length,
                'traits': traits,
                'states': states
            })

        for subclade in clade.clades:
            parse_clade(subclade, node_id)

    parse_clade(tree.root)
    return json.dumps(graph, indent=4)

# Example Nexus data with some nodes possibly missing traits or states
nexus_data = """
#NEXUS
Begin taxa;
    Dimensions ntax=4;
    TaxLabels Root Node1 Leaf1 Leaf2;
End;

Begin trees;
    Translate
        1 Root,
        2 Node1,
        3 Leaf1,
        4 Leaf2;
    tree tree1 = [&R] ((2[&states="active"]:0.1,3[&traits="yellow"]:0.1)1[&traits="red",states="active"]:0.2,4[&traits="blue",states="active"]:0.3);
End;
"""

json_output = nexus_to_json_with_traits_on_edges(nexus_data)
graph_data = json.loads(json_output)
print(json_output)
# Create and draw the graph
G = nx.DiGraph()
for node in graph_data['nodes']:
    G.add_node(node['id'], label=node['label'])
for edge in graph_data['edges']:
    G.add_edge(edge['source'], edge['target'], label=f"Traits: {edge['traits']}, States: {edge['states']}")

pos = nx.spring_layout(G)
nx.draw(G, pos, with_labels=True, labels=nx.get_node_attributes(G, 'label'), node_color='skyblue', node_size=2000, font_weight='bold', font_size=10, edge_color='gray')
edge_labels = nx.get_edge_attributes(G, 'label')
nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels, font_color='red')

plt.title('Phylogenetic Tree Visualization with Traits on Edges')
plt.axis('off')
plt.show()
