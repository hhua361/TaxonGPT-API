import json

# 物种映射关系
species_mapping = {
    "1": "Equisetum_arvense",
    "2": "Equisetum_fluviatile",
    "3": "Equisetum_hyemale",
    "4": "Equisetum_litorale",
    "5": "Equisetum_moorei",
    "6": "Equisetum_palustre",
    "7": "Equisetum_pratense",
    "8": "Equisetum_ramosissimum",
    "9": "Equisetum_sylvaticum",
    "10": "Equisetum_telmateia",
    "11": "Equisetum_trachyodon",
    "12": "Equisetum_variegatum",
    "13": "Extinct_Sphenopsida"
}

# 函数：从文件中加载JSON数据
def load_json(file_path):
    with open(file_path, 'r') as file:
        return json.load(file)

# 函数：保存JSON数据到文件
def save_json(data, file_path):
    with open(file_path, 'w') as file:
        json.dump(data, file, indent=4)

# 函数：用物种名替换节点编号
def replace_nodes_with_species_names(data):
    updated_data = []
    for entry in data:
        updated_entry = entry.copy()  # 复制原始条目
        updated_entry['Node1'] = species_mapping.get(entry['Node1'], entry['Node1'])  # 替换 Node1
        if 'Node2' in entry:
            updated_entry['Node2'] = species_mapping.get(entry['Node2'], entry['Node2'])  # 替换 Node2
        updated_data.append(updated_entry)
    return updated_data

# 文件路径
input_file_path = 'D:/桌面/TEST-KG/updated_knowledge_graph_2.json'  # 更改为您的JSON文件路径
output_file_path = 'D:/桌面/TEST-KG/updated_knowledge_graph_22.json'  # 更改为您希望保存更新后的JSON文件的路径

# 加载、处理和保存JSON数据
data = load_json(input_file_path)
updated_data = replace_nodes_with_species_names(data)
save_json(updated_data, output_file_path)
