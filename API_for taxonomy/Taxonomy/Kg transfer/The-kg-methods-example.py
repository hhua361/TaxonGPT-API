from Bio import Phylo
from io import StringIO
import networkx as nx
import json
import matplotlib.pyplot as plt

# 创建一个简单的树
tree = Phylo.Newick.Tree.from_clade(
    Phylo.Newick.Clade(name="Root", clades=[
        Phylo.Newick.Clade(name="Node1", clades=[
            Phylo.Newick.Clade(name="Leaf1"),
            Phylo.Newick.Clade(name="Leaf2"),
        ]),
        Phylo.Newick.Clade(name="Node2", clades=[
            Phylo.Newick.Clade(name="Leaf3"),
        ]),
    ])
)

# 保存为Nexus格式
handle = StringIO()
Phylo.write(tree, handle, "nexus")
nexus_data = handle.getvalue()

print("Nexus format data:")
print(nexus_data)

# 将树解析为有向图
def tree_to_graph(tree):
    G = nx.DiGraph()
    def add_clades(clade, parent=None):
        if parent:
            G.add_edge(parent, clade.name)
        if clade.name:
            G.add_node(clade.name)
        for subclade in clade.clades:
            add_clades(subclade, clade.name)

    add_clades(tree.root)
    return G

# 创建图
graph = tree_to_graph(tree)

# 输出图为JSON
def graph_to_json(graph):
    json_data = nx.node_link_data(graph)
    return json.dumps(json_data, indent=4)

json_output = graph_to_json(graph)
print("JSON format output:")
print(json_output)

# 加载 JSON 数据
data = json.loads(json_output)

# 创建有向图
G = nx.DiGraph()

# 添加节点
for node in data["nodes"]:
    G.add_node(node["id"])

# 添加边
for link in data["links"]:
    G.add_edge(link["source"], link["target"])

# 绘制图形
pos = nx.spring_layout(G, seed=42)  # 节点位置
nx.draw(G, pos, with_labels=True, node_size=2000, node_color='skyblue', font_size=10, font_weight='bold')
plt.title('Tree Structure Visualization from JSON Input')
plt.show()
