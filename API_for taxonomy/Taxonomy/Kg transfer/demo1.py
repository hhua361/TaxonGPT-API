import json
import networkx as nx
import matplotlib.pyplot as plt

# Load JSON data
with open("D:/桌面/Kg methods test/13-taxa-identifysteps-complexmodel.json") as f:
    data = json.load(f)

# Create directed graph
G = nx.DiGraph()

# Add nodes with captions and traits
for node in data['graph']['nodes']:
    # Extract traits if they exist within the node's properties
    traits = ", ".join(f"{prop['token']}={prop['type']['type']}" for prop in node.get('properties', []))
    G.add_node(node['id'], label=node['caption'], traits=traits)

# Add edges with relationship types
for rel in data['graph']['relationships']:
    G.add_edge(rel['fromId'], rel['toId'], label=rel['type'])

# Node positions using the layout information if available, else spring layout
pos = {node['id']: (node['position']['x'], node['position']['y']) for node in data['graph']['nodes']} if 'position' in data['graph']['nodes'][0] else nx.spring_layout(G)

# Draw the graph
plt.figure(figsize=(12, 8))
nx.draw(G, pos, with_labels=False, node_size=2000, node_color='lightblue', font_weight='bold', font_size=9, edge_color='gray')

# Draw custom labels
for node, (x, y) in pos.items():
    label = f"{G.nodes[node]['label']}\n{G.nodes[node]['traits']}"
    plt.text(x, y, label, fontsize=9, ha='center', va='center', bbox=dict(facecolor='white', edgecolor='black', boxstyle='round,pad=0.5'))

# Display edge labels
edge_labels = nx.get_edge_attributes(G, 'label')
nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels, font_color='red')

plt.title('Graph Visualization with Traits and Relationships')
plt.axis('off')  # Turn off the axis
plt.show()
