import dendropy
import json


def read_nexus_file(file_path):
    # 读取Nexus文件
    dataset = dendropy.DataSet.get(
        path=file_path,
        schema="nexus"
    )

    # 提取树和特征矩阵
    trees = dataset.tree_lists[0]
    char_matrices = dataset.char_matrices

    return trees, char_matrices


def extract_node_info_with_char(tree, char_matrix):
    node_info = {}

    for node in tree.preorder_node_iter():
        if node.taxon:
            node_data = {
                "label": node.taxon.label,
                "length": node.edge_length,
                "characters": {}
            }

            for char in char_matrix:
                if node.taxon in char_matrix.taxon_namespace:
                    char_value = char_matrix[char][node.taxon]
                    node_data["characters"][char.label] = char_value

            node_info[node.taxon.label] = node_data

    return node_info


def compare_sibling_characteristics(sibling1_char, sibling2_char):
    differences = {}

    for char in sibling1_char:
        if char in sibling2_char and sibling1_char[char] != sibling2_char[char]:
            differences[char] = (sibling1_char[char], sibling2_char[char])

    return differences


def extract_branch_characteristics(tree, node_info):
    branch_info = []

    for node in tree.preorder_node_iter():
        if node.child_nodes():
            for i in range(len(node.child_nodes()) - 1):
                child1 = node.child_nodes()[i]
                child2 = node.child_nodes()[i + 1]

                if child1.taxon and child2.taxon:
                    parent_label = node.taxon.label if node.taxon else None
                    child1_label = child1.taxon.label
                    child2_label = child2.taxon.label

                    child1_char = node_info[child1_label]["characters"]
                    child2_char = node_info[child2_label]["characters"]

                    branch_diff = compare_sibling_characteristics(child1_char, child2_char)

                    for char, (char1_value, char2_value) in branch_diff.items():
                        branch_info.append({
                            "source": parent_label,
                            "target": child1_label,
                            "length": child1.edge_length,
                            "character_changes": {char: char1_value}
                        })

                        branch_info.append({
                            "source": parent_label,
                            "target": child2_label,
                            "length": child2.edge_length,
                            "character_changes": {char: char2_value}
                        })

    return branch_info


def convert_to_knowledge_graph(node_info, branch_info):
    knowledge_graph = {"nodes": [], "edges": []}

    for node in node_info.values():
        node_entry = {
            "id": node["label"],
            "length": node["length"],
            "characters": node["characters"]
        }
        knowledge_graph["nodes"].append(node_entry)

    for branch in branch_info:
        edge_entry = {
            "source": branch["source"],
            "target": branch["target"],
            "length": branch["length"],
            "character_changes": branch["character_changes"]
        }
        knowledge_graph["edges"].append(edge_entry)

    return knowledge_graph


# 示例使用
file_path = "D:/桌面/taxonomy_primary_result/The_GPT-4_result/Dataset_2 (The Equisetum species (horsetails)) 3/DELTA_data/nexdata-1"
trees, char_matrices = read_nexus_file(file_path)

# 假设我们只处理第一棵树和第一个特征矩阵
tree = trees[0]
char_matrix = char_matrices[0]
node_info = extract_node_info_with_char(tree, char_matrix)
branch_info = extract_branch_characteristics(tree, node_info)

# 转换为JSON格式
knowledge_graph = convert_to_knowledge_graph(node_info, branch_info)
knowledge_graph_json = json.dumps(knowledge_graph, indent=4)

# 输出JSON
print(knowledge_graph_json)

# 保存为文件
with open("knowledge_graph.json", "w") as f:
    f.write(knowledge_graph_json)
