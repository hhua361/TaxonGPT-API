import json
from openai import OpenAI
import os
import re
import requests


client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
with open("D:/桌面/TEST-KG/nexus fix/matrix_knowledge_graph_22.json", "r", encoding="utf-8") as file:
    matrix_data = json.load(file)


# initial character分类结果存储为字典形式
initial_classification = {
    "1": ["Equisetum_litorale", "Equisetum_palustre"],
    "2": ["Equisetum_pratense", "Equisetum_hyemale", "Equisetum_moorei", "Equisetum_ramosissimum", "Equisetum_trachyodon", "Equisetum_variegatum"],
    "1 and 2": ["Equisetum_arvense", "Equisetum_telmateia", "Equisetum_sylvaticum", "Equisetum_fluviatile"]
}
groups = []
for state, species_list in initial_classification.items():
    groups.append(species_list)
for i, group in enumerate(groups, 1):
    print(f"Group {i} species:", group)
# group_1_species = groups[0]
# group_2_species = groups[1]
# group_3_species = groups[2]
# print(f"State 1: {group_1_species}",f"State 2: {group_2_species}",f"State 3: {group_3_species}")


# API调用函数，对于每个subgroup进行继续的分组
def classify_group(group_species):
    group_matrix = {species: matrix_data[species] for species in group_species}
    group_matrix_str = json.dumps(group_matrix, ensure_ascii=False)
    messages3 = [
            {"role": "system",
             "content":
                 """
                 You are a helpful taxonomist assistant.\n
                 You are skilled at calculating the correct information gain to choose the character that best divides species into even groups based on their states.\n
                 Based on the selected character, classify the species into different groups according to their states.\n
                 For each group with more than two species, continue selecting characters to further classify this group until each group only has one species.\n
                 After multiple classifications, determine the final classification levels and record each classifying character and its state.\n
                 Finally, generate a taxonomic key.
                 """},
            {"role": "system","content":
                """
                Generate the nested taxonomic key based on the provided morphological matrix. \n
                The process involves selecting a character to classify the species into groups. Repeat this classification within each subgroup until each group contains only one species.
                Information gain measures how much the uncertainty in the dataset is reduced after using a character for classification. It helps in selecting characters that minimize the entropy of the subset after classification, leading to better classification results.
                Please select the classification character for these group's species based on the morphological matrix and information gain methods.
                In the morphological matrix, 'Missing' and 'Not applicable' are invalid states. If a character has invalid states for the group being classified, it should be ignored.
                States are represented by numbers. For example, '1 and 2' means multiple states should be treated as a single state type and this multi-state characterization should not be confused with the single states within it (the state of '3' and '2 and 3' is different state, when you choose the character to based on the state to distinguish need to careful handle).The initial character should have no more than three state types.
                You need to calculate the information gain for each character and choose the highest information gain result. The higher the information gain result, the greater the contribution of the feature to the classification.
                After selecting the initial classification character and categorizing the species based on its state, repeat the process within each subgroup. For each subgroup, select the character with the highest information gain to further classify the species. Continue this process recursively until each group contains only one species.
                Now I will show you the morphological matrix. Please provide the classification character and the categorization of species based on its state. Then, continue to classify each subgroup recursively, showing the chosen character and categorization for each subgroup. Please present the result in a structured format, with each step clearly labeled.
                please don't show how you analysis and calculate, please show me the final result           
            """},
            {"role": "assistant",
             "content": """
                Understood. I will generate the nested taxonomic key based on the provided morphological matrix. Here is a summary of the steps I will follow:\n
                1. The matrix includes all species and their different states for each character.\n
                2. I will select a character to classify the species into groups and repeat this classification within each subgroup until each group contains only one species.\n
                3. I will use information gain to measure how much the uncertainty in the dataset is reduced after using a feature for classification. This helps in selecting features that minimize the entropy of the subset after classification, leading to better classification results.\n
                4. I will select the classification character for the group's species based on the morphological matrix and information gain methods.\n
                5. In the morphological matrix, 'Missing' and 'Not applicable' are considered invalid states. If a character has invalid states for the group being classified, it will be ignored.\n
                6. States are represented by numbers. For example, '2 and 3' means multiple states should be treated as a single state type, and This multi-state characterization should not be confused with the individual states(like '2', '3') within it (such as '3' and '2 and 3'  is the different state, these are two separate states, when i choose character to based on different state to distinguish the species). The classification character should have no more than three state types.\n
                7. I will use information gain to calculate all character and choose the highest information gain result, The higher the Information Gain result, the greater the contribution of the feature to the classification. \n
                8. The final result will provide only the initial classification character and the categorization of species based on its state. \n
                9. Don't need to show how the process about choose, only need to show the final result as nested structure, and i will store result in #character classify result# block
                Please provide the group morphological matrix data so that I can proceed with the classification.
             """},
            {"role": "user", "content": f"Here is the group information need to be classify and include the morphological matrix{group_matrix_str}"}
        ]
    response = client.chat.completions.create(
            model="gpt-4o",
            messages=messages3,
            stop=None,
            temperature=0,
            max_tokens=1000,
            n=1)
    result = response.choices[0].message.content
    print(f"API response for group {group_species}: {result}")
    return result

def recursive_classification(groups, final_classification, classification_results):
    while groups:
        try:
            state, current_group = groups.pop(0)
            print(f"Processing group with state: {state}, species: {current_group}")  # 调试信息
            if len(current_group) == 1:
                final_classification[current_group[0]] = current_group
            else:
                classification_result = classify_group(current_group)
                classification_results[state] = classification_result  # 存储API调用结果
        except Exception as e:
            print(f"Error processing group with state: {state}, species: {current_group}")  # 错误调试信息
            print(f"Exception: {e}")
            raise e
    return final_classification


# 假设之前已经初始化这些变量
groups = [
    ("1", ["Equisetum_litorale", "Equisetum_palustre"]),
    ("2", ["Equisetum_pratense", "Equisetum_hyemale", "Equisetum_moorei", "Equisetum_ramosissimum", "Equisetum_trachyodon", "Equisetum_variegatum"]),
    ("1 and 2", ["Equisetum_arvense", "Equisetum_telmateia", "Equisetum_sylvaticum", "Equisetum_fluviatile"])
]
final_classification = {}
classification_results = {}
print("Initial groups:", groups)
print("Initial final_classification:", final_classification)
print("Initial classification_results:", classification_results)

final_classification = recursive_classification(groups, final_classification, classification_results)
print("Final Classification:")
print(json.dumps(final_classification, indent=2, ensure_ascii=False))
print("\nClassification Results:")
print(json.dumps(classification_results, indent=2, ensure_ascii=False))

