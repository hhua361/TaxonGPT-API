from Bio import Phylo
from Bio.Phylo.Newick import Clade
from io import StringIO
import networkx as nx
import json
import matplotlib.pyplot as plt

# 创建更复杂的系统发育树
tree = Phylo.Newick.Tree.from_clade(
    Clade(name="Root", clades=[
        Clade(name="Node1", clades=[
            Clade(name="Leaf1"),
            Clade(name="Leaf2", clades=[
                Clade(name="SubLeaf1"),
                Clade(name="SubLeaf2")
            ]),
        ]),
        Clade(name="Node2", clades=[
            Clade(name="Leaf3"),
            Clade(name="Leaf4")
        ]),
        Clade(name="Node3", clades=[
            Clade(name="Leaf5", clades=[
                Clade(name="SubLeaf3"),
                Clade(name="SubLeaf4", clades=[
                    Clade(name="SubSubLeaf1"),
                    Clade(name="SubSubLeaf2")
                ])
            ])
        ])
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
pos = nx.spring_layout(G, seed=2)  # 节点位置
nx.draw(G, pos, with_labels=True, node_size=200, node_color='skyblue', font_size=10, font_weight='bold')
plt.title('Tree Structure Visualization from JSON Input')
plt.show()
