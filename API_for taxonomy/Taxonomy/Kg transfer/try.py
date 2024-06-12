import networkx as nx

# 创建有向图，因为树是有方向的结构
G = nx.DiGraph()

# 定义树结构和特征数据，这通常需要编程解析或手动输入
nodes = {
    "A": {"character1": "1", "character2": "0"},
    "B": {"character1": "0", "character2": "1"},
    "C": {"character1": "1", "character2": "1"},
    "D": {"character1": "0", "character2": "0"}
}
edges = [
    ("A", "B"),
    ("B", "C"),
    ("B", "D")
]

# 添加节点和边到图
for node, attrs in nodes.items():
    G.add_node(node, **attrs)

for src, dst in edges:
    G.add_edge(src, dst)

# 你可以将图导出为JSON或其他格式，或直接使用图进行分析和可视化
import matplotlib.pyplot as plt

# 可视化图
pos = nx.spring_layout(G)  # 为图布局
nx.draw(G, pos, with_labels=True, node_color='lightblue', edge_color='#909090', node_size=2000, font_size=10)
plt.title("Knowledge Graph of Phylogenetic Tree with Embedded Traits")
plt.show()
