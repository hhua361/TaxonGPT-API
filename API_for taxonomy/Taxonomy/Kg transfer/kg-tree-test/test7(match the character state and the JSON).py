import json

# 示例 character_info 字典，包含特征描述和状态
character_info = {
    "2": {
        "description": "the shoots <dimorphism>",
        "states": {
            "1": "conspicuously dimorphic: the c",
            "2": "distinguishable as fertile and",
            "3": "all green and alike vegetative"
        }
    },
    "5": {
        "description": "the main stems <of the assimil",
        "states": {
            "1": "bright green",
            "2": "dull green"
        }
    },
    "20": {
        "description": "the primary branches <carriage",
        "states": {
            "1": "ascending",
            "2": "spreading",
            "3": "drooping"
        }
    },
    "22": {
        "description": "the first <primary> branch int",
        "states": {
            "1": "much shorter than the subtendi",
            "2": "at least as long as the subten"
        }
    }
}

# 示例知识图谱条目
knowledge_graph_entry = {
    "Parent": "node4",
    "Node1": "node5",
    "Differences1": {
        "2": "1",
        "5": "(1 2)",
        "20": "2",
        "22": "1"
    },
    "Node2": "node24",
    "Differences2": {
        "2": "2",
        "5": "1",
        "20": "(2 3)",
        "22": "2"
    }
}

def replace_indices_with_descriptions(differences, character_info):
    updated_differences = {}
    for feature_index, state_indices in differences.items():
        feature_index = str(feature_index)
        if feature_index in character_info:
            description = character_info[feature_index]["description"]
            # 处理可能的多状态
            states = state_indices.strip("()").split()
            state_descriptions = " / ".join([character_info[feature_index]["states"].get(state, "Unknown state") for state in states])
            updated_differences[description] = state_descriptions
    return updated_differences

# 更新知识图谱中的特征和状态描述
updated_differences1 = replace_indices_with_descriptions(knowledge_graph_entry["Differences1"], character_info)
updated_differences2 = replace_indices_with_descriptions(knowledge_graph_entry["Differences2"], character_info)

# 打印更新后的知识图谱条目
print("Updated Differences for Node1:")
print(json.dumps(updated_differences1, indent=4))
print("Updated Differences for Node2:")
print(json.dumps(updated_differences2, indent=4))
