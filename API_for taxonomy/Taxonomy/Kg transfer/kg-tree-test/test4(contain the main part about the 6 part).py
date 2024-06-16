import re
import json


### Reading files and extracting parts ###
def read_nexus_file(file_path):
    with open(file_path, 'r') as file:
        return file.read()
def extract_section(content, section_name):
    # 定义正则表达式模式，用于匹配指定部分的内容
    pattern = rf'BEGIN {section_name};(.*?)END;'
    # 使用正则表达式搜索匹配的部分
    match = re.search(pattern, content, re.DOTALL)
    # 如果找到匹配的部分，则返回其内容，去掉前后空白字符；否则返回None
    return match.group(1).strip() if match else None

# 测试读取文件和提取部分内容
nexus_file_path = "D:/桌面/TEST-KG/nexus fix/ancestral_states.nex"
# 读取NEXUS文件内容
content = read_nexus_file(nexus_file_path)
# 提取TAXA部分的内容
taxa_content = extract_section(content, 'TAXA')
# 提取CHARACTERS部分的内容
characters_content = extract_section(content, 'CHARACTERS')
# 提取TREES部分的内容
trees_content = extract_section(content, 'TREES')

"""
print(taxa_content)
print(characters_content)
print(trees_content)
"""


### Parsing the Taxa section ###
def parse_taxa_section(taxa_content):
    # 使用正则表达式匹配TAXLABELS和随后的所有标签，直到遇到分号
    taxa_labels = re.findall(r'TAXLABELS\s*(.*?);', taxa_content, re.DOTALL)
    # 将匹配到的标签字符串分割成单独的标签，并去除前后空白字符
    taxa_list = [label.strip() for label in taxa_labels[0].split()]
    # 返回包含Taxa标签的字典
    return {'Taxa': taxa_list}
# 测试解析Taxa部分
taxa = parse_taxa_section(taxa_content)
# print(taxa)


### Parsing the Characters section ###
def parse_characters_section(characters_content):
    # 使用正则表达式匹配MATRIX部分的内容
    matrix_match = re.search(r'MATRIX(.*?);', characters_content, re.DOTALL)
    if not matrix_match:
        raise ValueError("MATRIX section not found in characters content")
    matrix = matrix_match.group(1).strip()

    # 初始化用于存储MATRIX数据的字典
    matrix_dict = {}
    current_taxon = None
    current_features = []
    # 逐行解析MATRIX部分的内容
    for line in matrix.split('\n'):
        if line.strip():
            parts = line.split()
            taxon = parts[0]
            features = ' '.join(parts[1:])

            if current_taxon is None:
                # 第一个taxon
                current_taxon = taxon
                current_features.append(features)
            elif taxon in matrix_dict:
                # 后续行属于上一个taxon
                current_features.append(features)
            else:
                # 新的taxon开始
                matrix_dict[current_taxon] = ''.join(current_features)
                current_taxon = taxon
                current_features = [features]

    # 保存最后一个taxon
    if current_taxon is not None:
        matrix_dict[current_taxon] = ''.join(current_features)

    return {'Matrix': matrix_dict}

# 测试解析Characters部分
characters = parse_characters_section(characters_content)
print(characters)


###  Parsing Tree Structures section ###
def parse_trees_section(trees_content):
    tree = re.search(r'TREE (.*?) = (.*?);', trees_content, re.DOTALL).group(2).strip()
    return {'Tree': tree}

# 测试解析树结构部分
trees = parse_trees_section(trees_content)
# print(trees)


### Comparing character ###
def normalize_multi_state_feature(feature):
    # 去除多状态特征中的空格并排序
    # 去除括号和空格，并将状态分割成列表
    states = feature.replace('(', '').replace(')', '').replace(' ', '').split()
    # 对状态进行排序并重新组合成字符串
    return f"({' '.join(sorted(states))})"

def compare_features(char_matrix, node1, node2):
    differences1 = {}   # 存储第一个节点的不同特征
    differences2 = {}   # 存储第二个节点的不同特征

    features1 = char_matrix[node1]   # 第一个节点的特征字符串
    features2 = char_matrix[node2]   # 第二个节点的特征字符串

    i = 1  # 特征索引从1开始
    j1 = j2 = 0  # 用于遍历特征字符串的指针

    while j1 < len(features1) and j2 < len(features2):
        if features1[j1] == '(' and features2[j2] == '(':
            # 处理多状态特征
            end1 = features1.find(')', j1)
            end2 = features2.find(')', j2)
            normalized1 = normalize_multi_state_feature(features1[j1:end1+1])
            normalized2 = normalize_multi_state_feature(features2[j2:end2+1])
            if normalized1 != normalized2:
                differences1[i] = normalized1
                differences2[i] = normalized2
            j1 = end1 + 1
            j2 = end2 + 1
        elif features1[j1] == '(':
            # 处理只有node1有多状态特征的情况
            end1 = features1.find(')', j1)
            normalized1 = normalize_multi_state_feature(features1[j1:end1+1])
            differences1[i] = normalized1
            j1 = end1 + 1
            differences2[i] = features2[j2]
            j2 += 1
        elif features2[j2] == '(':
            # 处理只有node2有多状态特征的情况
            end2 = features2.find(')', j2)
            normalized2 = normalize_multi_state_feature(features2[j2:end2+1])
            differences2[i] = normalized2
            j2 = end2 + 1
            differences1[i] = features1[j1]
            j1 += 1
        else:
            # 处理单状态特征
            if features1[j1] != features2[j2]:
                differences1[i] = features1[j1]
                differences2[i] = features2[j2]
            j1 += 1
            j2 += 1
        i += 1

    return differences1, differences2

"""
# 测试比较特征
node1 = 'node9'
node2 = 'Equisetum_palustre'
char_matrix = {
    'node9': '13(12)1(12)212212211121(12)21112211(34)11',
    'Equisetum_palustre': '13-(1 2)?2(1 2 3)222212?111(1 2)(1 2)(1 2)112211(2 3 4)11'
}
differences1, differences2 = compare_features(char_matrix, node1, node2)
print(differences1)
print(differences2)
"""


### Recursively traverse the tree structure and find the relationship about the subnodes ###
def parse_newick_to_relationships(newick):
    relationships = {}   # 用于存储节点关系的字典

    def parse_subtree(subtree, parent=None):
        # Debug输出以跟踪解析进度
        # print(f"Parsing subtree: {subtree}, Parent: {parent}")

        # 如果子树有括号，去除外围括号
        if subtree.startswith('(') and subtree.endswith(')'):
            subtree = subtree[1:-1]

        balance = 0   # 用于跟踪括号平衡
        last_split = 0   # 上一次分割的位置
        children = []   # 子节点列表

        # 遍历子树字符串，找到子节点
        for i, char in enumerate(subtree):
            if char == '(':
                balance += 1
            elif char == ')':
                balance -= 1
            elif char == ',' and balance == 0:
                # 在平衡状态下找到逗号，分割子节点
                children.append(subtree[last_split:i].strip())
                last_split = i + 1
        # 添加最后一个子节点
        children.append(subtree[last_split:].strip())

        # 处理子节点
        child_nodes = []   # 子节点名称列表
        for child in children:
            if '(' in child:
                closing_index = child.rfind(')')
                node_name = child[closing_index + 1:].strip()
                child_subtree = child[:closing_index + 1]
                if not node_name:
                    # 如果子节点没有名称，生成一个默认名称
                    node_name = f'node{len(relationships) + 1}'
                child_nodes.append(node_name)
                parse_subtree(child_subtree, node_name)
            else:
                child_nodes.append(child)

        if parent:
            # 将子节点列表添加到父节点的关系字典中
            relationships[parent] = child_nodes

        return parent

    # 解析最外层的树
    if newick.startswith('(') and ')' in newick:
        closing_index = newick.rfind(')')
        root_name = newick[closing_index + 1:].strip()
        if not root_name:
            root_name = "root"
        parse_subtree(newick[:closing_index + 1], root_name)

    return relationships


# 测试解析 Newick 树结构
tree_structure = '(1,((((((2,4)node9,6)node8,((((3,11)node16,5)node15,12)node14,8)node13)node7,13)node6,10)node5,(7,9)node24)node4)node2'
relationships = parse_newick_to_relationships(tree_structure)
print(json.dumps(relationships, indent=4))



### 记录每个子节点的字符状态差异  ###
def build_knowledge_graph(relationships, char_matrix):
    knowledge_graph = []
    visited = set()  # 创建一个集合用来记录访问过的节点

    def traverse_and_compare(parent, children):
        if len(children) == 2:
            node1, node2 = children
            if {node1, node2}.issubset(visited):
                return  # 如果两个子节点都已访问过，跳过当前遍历

            differences1, differences2 = compare_features(char_matrix, node1, node2)
            knowledge_graph.append({
                'Parent': parent,
                'Node1': node1,
                'Differences1': differences1,
                'Node2': node2,
                'Differences2': differences2
            })
            visited.update([node1, node2])  # 更新访问过的节点集合

            if node1 in relationships and node1 not in visited:
                traverse_and_compare(node1, relationships[node1])
            if node2 in relationships and node2 not in visited:
                traverse_and_compare(node2, relationships[node2])

    for parent, children in relationships.items():
        if parent not in visited:  # 检查父节点是否已经访问过
            traverse_and_compare(parent, children)

    return knowledge_graph

# 示例特征矩阵
char_matrix = {
    '1': '(1 2)12(1 2)1212?22(1 2)21?1?12(2 3)121211113',
    '2': '(1 2)3-1?3(1 3)2?1231?(1 2)2?2211?2211(3 4)11',
    '3': '23-121311?2(2 3)312?2------121(4 5)2-',
    '4': '13-1?212?12(1 2)1?12?(1 2)211(1 2)2212-11',
    '5': '23-121322?2(2 3)?21?1------122-2-',
    '6': '13-(1 2)?2(1 2 3)222212?111(1 2)(1 2)(1 2)112211(2 3 4)11',
    '7': '22?1?1(1 3)2??2(2 3)2???112(2 3)121211112',
    '8': '23-??(1 2)112?2(2 3)3???1?2??12121(2 3 4 5)2-',
    '9': '(1 2)2?11(2 3)(1 3)22?2(2 3)2??11123221211(1 2)12',
    '10': '(1 2)111??12212(2 3)2?111122111211112',
    '11': '23-(1 2)?1(2 3)12?213?211???1??122-2-',
    '12': '23-(1 2)?2(2 3)12?213?111???1??121(4 5)2-',
    '13': '?--???????2??????------??--?-',
    'node9': '13(12)1(12)212212211121(12)21112211(34)11',
    'node8': '13(12)1(12)2122(12)2221111(12)2(12)112211(34)11',
    'node16': '23(12)121312(12)2231211(12)2(12)11212(12)42(12)',
    'node15': '23(12)121312(12)2231111(12)2(12)11212(12)42(12)',
    'node14': '23(12)1(12)2312(12)2231111(12)2(12)11212142(12)',
    'node13': '23(12)1(12)2112(12)2231111(12)2(12)112121(34)2(12)',
    'node7': '23(12)1(12)2122(12)2221111(12)2(12)112211(34)1(12)',
    'node6': '2(34)(12)1(12)2122(12)2221111(12)2(12)11(12)211(1234)1(12)',
    'node5': '21(12)1(12)2122(12)2221111122111211112',
    'node24': '22(12)112122(12)222111112(23)121211112',
    'node4': '21(12)112122(12)222111112(23)121211112',
    'node2': '21(12)112122(12)222111112(23)12121111(23)'
}

# 父子节点关系示例
relationships = {
    "node9": ["2", "4"],
    "node8": ["node9", "6"],
    "node16": ["3", "11"],
    "node15": ["node16", "5"],
    "node14": ["node15", "12"],
    "node13": ["node14", "8"],
    "node7": ["node8", "node13"],
    "node6": ["node7", "13"],
    "node5": ["node6", "10"],
    "node24": ["7", "9"],
    "node4": ["node5", "node24"],
    "node2": ["1", "node4"]
}
# 构建知识图谱
knowledge_graph = build_knowledge_graph(relationships, char_matrix)
print(json.dumps(knowledge_graph, indent=4))

output_path = "D:/桌面/TEST-KG/33333.json"
with open(output_path, 'w') as f:
    json.dump(knowledge_graph, f, indent=4)
output_path













