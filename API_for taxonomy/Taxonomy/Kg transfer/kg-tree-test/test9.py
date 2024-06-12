import json

# Load the JSON file
file_path = '/mnt/data/2222222'
with open(file_path, 'r', encoding='utf-8') as file:
    data = json.load(file)


# Function to build the tree from knowledge graph
def build_tree(data):
    nodes = {}
    relationships = []

    # Create nodes and relationships
    for item in data:
        parent = item['Parent']
        node1 = item['Node1']
        node2 = item['Node2']

        if parent not in nodes:
            nodes[parent] = {'children': []}
        if node1 not in nodes:
            nodes[node1] = {'children': []}
        if node2 not in nodes:
            nodes[node2] = {'children': []}

        nodes[parent]['children'].append(node1)
        nodes[parent]['children'].append(node2)
        relationships.append((parent, node1))
        relationships.append((parent, node2))

    # Find the root node (a node that is never a child)
    all_nodes = set(nodes.keys())
    children_nodes = set(node for parent, child in relationships for node in (child,))
    root_nodes = all_nodes - children_nodes

    # Assuming there's a single root node, we select it
    root_node = root_nodes.pop() if root_nodes else None

    return root_node, nodes


root_node, tree = build_tree(data)
root_node, tree
