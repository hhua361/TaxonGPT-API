import re
import json

# 读取初始字符信息
with open("D:/桌面/TEST-KG/nexus fix/initial_character_info", "r", encoding="utf-8") as file:
    initial_character = file.read()
# 读取形态学矩阵信息
with open("D:/桌面/TEST-KG/nexus fix/matrix_knowledge_graph_22.json", "r", encoding="utf-8") as file:
    data = json.load(file)

# 定义用于解析API响应结果的函数
def parse_classification_result(result_text):
    classification = {}
    # 使用正则表达式匹配每个状态块
    state_sections = re.findall(r'- \*\*State: ([\d\s\w&]+)\*\*\n((?:\s*-\s[A-Za-z_]+\n)+)', result_text)
    for state, species_block in state_sections:
        # 匹配物种列表
        species_list = re.findall(r'- ([A-Za-z_]+)', species_block)
        classification[state.strip()] = species_list
    return classification

# 解析初始分类结果
parsed_initial_classification = parse_classification_result(initial_character)
print(parsed_initial_classification)

"""# 示例输出解析结果
for state, species in parsed_initial_classification.items():
    print(f"State {state}: {', '.join(species)}")"""