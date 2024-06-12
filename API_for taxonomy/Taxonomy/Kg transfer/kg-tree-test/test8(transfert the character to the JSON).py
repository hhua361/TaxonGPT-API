import json

# 函数：从文件中加载JSON数据
def load_json(file_path):
    with open(file_path, 'r') as file:
        return json.load(file)

# 函数：将特征索引和状态索引替换为描述性文本
def replace_indices_with_descriptions(differences, character_info):
    updated_differences = {}
    for feature_index, state_indices_list in differences.items():
        feature_index = str(feature_index)
        if feature_index in character_info:
            description = character_info[feature_index]["description"]
            all_state_descriptions = []
            for state_indices in state_indices_list:
                # 检查并处理复合状态
                if state_indices.startswith("(") and state_indices.endswith(")"):
                    # 去除括号，分割状态
                    states = state_indices.strip("()").split(',')
                    state_descriptions = []
                    for state in states:
                        # 对每个单独的状态获取描述
                        if state.strip() in character_info[feature_index]["states"]:
                            state_descriptions.append(character_info[feature_index]["states"][state.strip()])
                        else:
                            state_descriptions.append("Unknown state")
                    if state_descriptions:
                        combined_description = " / ".join(state_descriptions)
                        all_state_descriptions.append(combined_description)
                else:
                    # 处理单一状态或未知状态
                    if state_indices in character_info[feature_index]["states"]:
                        all_state_descriptions.append(character_info[feature_index]["states"][state_indices])
                    elif state_indices.strip():
                        all_state_descriptions.append("Unknown state")

            # 清除多余的未知状态，只保留实际的状态描述
            filtered_descriptions = [desc for desc in all_state_descriptions if desc != "Unknown state"]
            updated_differences[description] = filtered_descriptions if filtered_descriptions else ["Unknown state"]
    return updated_differences

# 函数：处理并返回更新后的知识图谱条目
def update_knowledge_graph_entry(entry, character_info):
    updated_entry = {
        "Parent": entry["Parent"],
        "Node1": entry["Node1"],
        "Differences1": replace_indices_with_descriptions(entry["Differences1"], character_info),
        "Node2": entry["Node2"],
        "Differences2": replace_indices_with_descriptions(entry["Differences2"], character_info)
    }
    return updated_entry

# 主函数
def main(character_info_path, knowledge_graph_path, output_path):
    # 加载 JSON 文件
    character_info = load_json(character_info_path)
    knowledge_graph = load_json(knowledge_graph_path)

    # 处理每个知识图谱条目
    updated_knowledge_graph = [update_knowledge_graph_entry(entry, character_info) for entry in knowledge_graph]

    # 将更新后的知识图谱保存为新的 JSON 文件
    with open(output_path, 'w') as f:
        json.dump(updated_knowledge_graph, f, indent=4)

    print(f"Updated knowledge graph saved to {output_path}")

# 示例文件路径
character_info_path="D:/桌面/TEST-KG/character_info.json"
knowledge_graph_path="D:/桌面/TEST-KG/33333.json"
output_path = "D:/桌面/TEST-KG/updated_knowledge_graph_2.json"

# 调用主函数
main(character_info_path, knowledge_graph_path, output_path)
