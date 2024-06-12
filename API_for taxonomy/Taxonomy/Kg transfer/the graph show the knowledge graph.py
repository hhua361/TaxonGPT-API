import json
import networkx as nx
import matplotlib.pyplot as plt

# 示例 JSON 数据字符串
json_data = """
{
  "taxa": ["A", "B", "C", "D"],
  "characters": [
    {"id": "character1", "states": {"A": "1", "B": "0", "C": "1", "D": "0"}},
    {"id": "character2", "states": {"A": "0", "B": "1", "C": "1", "D": "0"}}
  ],
  "trees": [
    {
      "name": "myTree",
      "structure": "(A,(B,(C,D)));",
      "annotations": {
        "A": {"character1": "1", "character2": "0"},
        "B": {"character1": "0", "character2": "1"},
        "C": {"character1": "1", "character2": "1"},
        "D": {"character1": "0", "character2": "0"}
      }
    }
  ]
}
"""

data = json.loads(json_data)
G = nx.DiGraph()


def add_edges(structure, parent=None):
    depth = 0  # Ensure depth is initialized outside the loop
    structure = structure.strip(';')
    if structure.startswith('(') and structure.endswith(')'):
        structure = structure[1:-1]

    i, n = 0, len(structure)
    last_i = 0  # Start index of the current node string

    while i < n:
        if structure[i] == '(':
            depth += 1
        elif structure[i] == ')':
            depth -= 1
        elif structure[i] == ',' and depth == 0:
            # Process the node or subtree before the comma
            node_name = structure[last_i:i].strip()
            if '(' in node_name:
                node_name = node_name.split('(')[0]
            if parent:
                G.add_node(node_name)
                G.add_edge(parent, node_name)
            add_edges(structure[last_i:i].strip(), node_name)
            last_i = i + 1  # Update start index after the comma

        i += 1

    # Add the last node or subtree after the last comma
    if last_i < n:
        node_name = structure[last_i:n].strip()
        if '(' in node_name:
            node_name = node_name.split('(')[0]
        if parent:
            G.add_node(node_name)
            G.add_edge(parent, node_name)
        add_edges(structure[last_i:n].strip(), node_name)


# 解析树结构
for tree in data['trees']:
    add_edges(tree['structure'])

# 添加节点注释
for node in G.nodes():
    annotations = data['trees'][0]['annotations'].get(node, {})
    label = ', '.join(f"{k}: {v}" for k, v in annotations.items())
    G.nodes[node]['label'] = node + (' (' + label + ')' if label else '')

# 绘制图形
pos = nx.spring_layout(G, seed=42)  # 节点位置
nx.draw(G, pos, labels=nx.get_node_attributes(G, 'label'), with_labels=True, node_size=2000, node_color='skyblue',
        font_size=10, font_weight='bold')
plt.title('Tree Structure Visualization from JSON Input')
plt.show()
