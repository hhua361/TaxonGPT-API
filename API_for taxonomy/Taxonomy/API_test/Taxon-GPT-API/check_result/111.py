import json

# 示例输入，实际为JSON字符串，需要先转换为字典
input_data = {
    '1': '{\n    "Character": "Character2",\n    "States": {\n        "1": ["Huperzia selago"],\n        "2": {\n            "Character": "Character12",\n            "States": {\n                "1": ["Lycopodium clavatum"],\n                "2": {\n                    "Character": "Character9",\n                    "States": {\n                        "1": {\n                            "Character": "Character5",\n                            "States": {\n                                "2": ["Diphasiastrum alpinum"],\n                                "3": ["Diphasiastrum complanatum"]\n                            }\n                        },\n                        "2": {\n                            "Character": "Character20",\n                            "States": {\n                                "1": ["Lycopodiella inundata"],\n                                "2 and 3": ["Lycopodium annotinum"]\n                            }\n                        }\n                    }\n                }\n            }\n        },\n        "3": {\n            "Character": "Character8",\n            "States": {\n                "1": {\n                    "Character": "Character4",\n                    "States": {\n                        "1": ["Selaginella kraussiana"],\n                        "2": ["Selaginella selaginoides"]\n                    }\n                }\n            }\n        }\n    }\n}',
    '2': '{\n    "Character": "Character20",\n    "States": {\n        "1": ["Isoetes histrix"],\n        "2 and 3": ["Isoetes lacustris"],\n        "1 and 2 and 3": ["Isoetes echinospora"]\n    }\n}'
}

# 将输入字符串转换为字典
classification_result = {key: json.loads(value) for key, value in input_data.items()}

# 递归函数将结构转换为所需格式
def convert_structure(node):
    if "Character" in node and "States" in node:
        character = node["Character"]
        states = node["States"]
        converted = {f"Character {character.replace('Character', '')}": {}}
        for state, sub_node in states.items():
            state_key = f"State {state}"
            if isinstance(sub_node, list):
                converted[f"Character {character.replace('Character', '')}"][state_key] = sub_node[0] if len(sub_node) == 1 else sub_node
            elif isinstance(sub_node, dict):
                converted[f"Character {character.replace('Character', '')}"][state_key] = convert_structure(sub_node)
        return converted
    return node

# 处理分类检索表
converted_result = {}
for key, value in classification_result.items():
    converted_result[f"Character {key}"] = convert_structure(value)

# 打印更新后的分类检索表
print("Updated Classification Key:")
classification_key = json.dumps(converted_result, indent=4, ensure_ascii=False)

import json
def replace_indices_with_descriptions_in_key(key, character_info, parent_char_index=None):
    updated_key = {}
    for char_state, subtree in key.items():
        if char_state.startswith("Character"):
            parts = char_state.split()
            if len(parts) > 1:
                char_index = parts[1]
                if char_index in character_info:
                    char_description = f"Character {char_index}: {character_info[char_index]['description']}"
                    if isinstance(subtree, dict):
                        updated_subtree = replace_indices_with_descriptions_in_key(subtree, character_info, char_index)
                        updated_key[char_description] = updated_subtree
                    else:
                        updated_key[char_description] = subtree
                else:
                    updated_key[char_state] = subtree
            else:
                updated_key[char_state] = subtree
        elif char_state.startswith("State") and parent_char_index:
            states = char_state.split()[1:]
            state_descriptions = []
            for state in states:
                individual_states = state.split("and")
                descriptions = [character_info[parent_char_index]["states"].get(s.strip(), "") for s in individual_states]
                state_descriptions.append(" and ".join(filter(None, descriptions)))
            state_key = f"State {' '.join(states)}: {' / '.join(state_descriptions)}"
            if isinstance(subtree, dict):
                updated_key[state_key] = replace_indices_with_descriptions_in_key(subtree, character_info, parent_char_index)
            else:
                updated_key[state_key] = subtree
        else:
            updated_key[char_state] = subtree
    return updated_key

# 处理分类检索表
updated_classification_key = replace_indices_with_descriptions_in_key(classification_key, character_info)

# 打印更新后的分类检索表
print("Updated Classification Key:")
print(json.dumps(updated_classification_key, indent=4))

