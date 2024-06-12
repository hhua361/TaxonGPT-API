from Bio import Phylo
from Bio.Phylo.Newick import Clade
from io import StringIO
import networkx as nx
import json
import matplotlib.pyplot as plt

# 创建更复杂的系统发育树，使用comment属性存储性状和状态
tree = Phylo.Newick.Tree.from_clade(
    Clade(name="Root", comment='traits="typeA", states="active"', clades=[
        Clade(name="Node1", comment='traits="typeB", states="inactive"', clades=[
            Clade(name="Leaf1", comment='traits="typeC", states="active"'),
            Clade(name="Leaf2", comment='traits="typeC", states="inactive"', clades=[
                Clade(name="SubLeaf1", comment='traits="typeD", states="active"'),
                Clade(name="SubLeaf2", comment='traits="typeD", states="inactive"')
            ]),
        ]),
        Clade(name="Node2", comment='traits="typeB", states="active"', clades=[
            Clade(name="Leaf3", comment='traits="typeE", states="inactive"'),
            Clade(name="Leaf4", comment='traits="typeE", states="active"')
        ]),
        Clade(name="Node3", comment='traits="typeF", states="active"', clades=[
            Clade(name="Leaf5", comment='traits="typeG", states="inactive"', clades=[
                Clade(name="SubLeaf3", comment='traits="typeH", states="active"'),
                Clade(name="SubLeaf4", comment='traits="typeH", states="inactive"', clades=[
                    Clade(name="SubSubLeaf1", comment='traits="typeI", states="active"'),
                    Clade(name="SubSubLeaf2", comment='traits="typeI", states="inactive"')
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
        node_id = clade.name or id(clade)
        # 提取性状和状态信息
        traits = clade.comment.split(", ")[0].split("=")[1] if clade.comment else ""
        states = clade.comment.split(", ")[1].split("=")[1] if clade.comment else ""
        G.add_node(node_id, name=clade.name, traits=traits, states=states)
        if parent:
            G.add_edge(parent, node_id)
        for subclade in clade.clades:
            add_clades(subclade, node_id)

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

data = json.loads(json_output)

# 创建有向图
G = nx.DiGraph()

# 添加节点
for node in data["nodes"]:
    G.add_node(node["id"], name=node["name"], traits=node["traits"], states=node["states"])

# 添加边
for link in data["links"]:
    G.add_edge(link["source"], link["target"])

# 计算节点位置
pos = nx.spring_layout(G, seed=22)  # 节点位置

# 绘制图形，不包含自定义标签
nx.draw(G, pos, with_labels=False, node_size=200, node_color='skyblue', font_size=10, font_weight='bold')

# 添加自定义标签
for node_id in G.nodes:
    node = G.nodes[node_id]
    label = f"{node['name']} ({node['traits']}, {node['states']})"
    plt.text(pos[node_id][0], pos[node_id][1]+0.1, label, color='black', ha='center')

plt.title('Tree Structure Visualization from JSON Input')
plt.show()
