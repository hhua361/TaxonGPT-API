import networkx as nx
import json
from Bio import Phylo

def parse_nexus_to_graph(nexus_file):
    # 使用Biopython读取Nexus文件
    tree = Phylo.read(nexus_file, 'nexus')
    G = nx.DiGraph()

    # 为每个Clade创建节点，并添加边
    for clade in tree.find_clades():
        if clade.name:
            G.add_node(clade.name, traits=clade.comment)  # 假设注释中有性状信息

        if clade.confidence and clade.name:
            # 假设confidence作为父节点名称
            parent_name = clade.confidence
            if parent_name in G:
                G.add_edge(parent_name, clade.name)

    return G

def graph_to_json(graph):
    # 将图转换为JSON格式
    json_data = nx.node_link_data(graph)
    return json.dumps(json_data, indent=4)

def main():
    nexus_file = 'path_to_your_nexus_file.nex'  # Nexus文件路径
    graph = parse_nexus_to_graph(nexus_file)
    json_output = graph_to_json(graph)
    print(json_output)

    # 将JSON输出到文件
    with open('output.json', 'w') as f:
        f.write(json_output)

if __name__ == '__main__':
    main()
