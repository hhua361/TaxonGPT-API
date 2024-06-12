import json
import networkx as nx
import matplotlib.pyplot as plt

# Load the JSON data
file_path = "D:/桌面/taxonomy_primary_result/The_GPT-4_result/Dataset_3 (The Lycopodiales (Diphasiastrum, Huperzia, Isoetes, Lycopodium, Selaginella)) 4/Information gain methods/matrix_knowledge_graph.json"
with open(file_path, 'r') as file:
    data = json.load(file)

# Create the directed graph
G = nx.DiGraph()

# Add nodes and edges based on the characteristics
for entity, details in data.items():
    for characteristic, value in details['Characteristics'].items():
        G.add_node(entity)
        if isinstance(value, str) and 'and' in value:
            values = value.split(' and ')
            for v in values:
                G.add_edge(entity, f"{characteristic}-{v}")
        else:
            G.add_edge(entity, f"{characteristic}-{value}")

# Draw the graph
plt.figure(figsize=(12, 12))
pos = nx.spring_layout(G)
nx.draw(G, pos, with_labels=True, node_color='skyblue', node_size=3000, font_size=10, font_weight='bold', edge_color='gray')
plt.title("Knowledge Graph")
plt.show()