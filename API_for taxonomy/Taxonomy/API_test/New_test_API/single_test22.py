import json
from openai import OpenAI
import os
import re

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
# 输入对应的起始的character
with open("D:/桌面/TEST-KG/nexus fix/initial_character_info", "r") as file:
    initial_character = file.read()
# 定义一个用于解析API响应结果的function
def parse_classification_result(result_text):
    classification = {}
    state_sections = re.findall(r'\*\*State "([^"]+)"\*\*:\n(.*?)\n\n', result_text, re.DOTALL)
    for state, species_block in state_sections:
        species_list = re.findall(r'- ([A-Za-z_]+)', species_block)
        classification[state] = species_list
    return classification
parsed_initial_classification = parse_classification_result(initial_character)
print(parsed_initial_classification)

with open("D:/桌面/TEST-KG/nexus fix/matrix_knowledge_graph_22.json", "r") as file:
    data = json.load(file)

    messages = [
            {"role": "system",
             "content":"""
                 You are a helpful taxonomist assistant.\n
                 You are skilled at calculating the correct information gain to choose the character that best divides species into even groups based on their states.\n
                 Based on the selected character, classify the species into different groups according to their states.\n
                 For each group with more than two species, continue selecting characters to further classify this group until each group only has one species.\n
                 After multiple classifications, determine the final classification levels and record each classifying character and its state.\n
                 Finally, generate a taxonomic key.
                 """},
            {"role": "system","content":"""
                Generate the taxonomic key based on the provided morphological matrix. \n
                The process involves selecting a character to classify the species into groups. Repeat this classification within each subgroup until each group contains only one species.
                Information gain measures how much the uncertainty in the dataset is reduced after using a character for classification. It helps in selecting characters that minimize the entropy of the subset after classification, leading to better classification results.
                Please select the classification character for these group's species based on the morphological matrix and information gain methods.
                In the morphological matrix, 'Missing' and 'Not applicable' are invalid states. If a character has invalid states for the group being classified, it should be ignored.
                States are represented by numbers. For example, '1 and 2' means multiple states should be treated as a single state type and this multi-state characterization should not be confused with the single states within it.The initial character should have no more than three state types.
                You need to calculate the information gain for each character and choose the highest information gain result. The higher the information gain result, the greater the contribution of the feature to the classification.
                After selecting the initial classification character and categorizing the species based on its state, repeat the process within each subgroup. For each subgroup, select the character with the highest information gain to further classify the species. Continue this process recursively until each group contains only one species.
                Now I will show you the morphological matrix. Please provide the classification character and the categorization of species based on its state. Then, continue to classify each subgroup recursively, showing the chosen character and categorization for each subgroup. Please present the result in a structured format, with each step clearly labeled.
                please don't show how you analysis and calculate, please show me the final result           
            """},
            {"role": "assistant",
             "content": """
                        Understood. I will generate the taxonomic key based on the provided morphological matrix. Here is a summary of the steps I will follow:\n
                        1. The matrix includes all species and their different states for each character.\n
                        2. I will select a character to classify the species into groups and repeat this classification within each subgroup until each group contains only one species.\n
                        3. I will use information gain to measure how much the uncertainty in the dataset is reduced after using a feature for classification. This helps in selecting features that minimize the entropy of the subset after classification, leading to better classification results.\n
                        4. I will select the classification character for the group's species based on the morphological matrix and information gain methods.\n
                        5. In the morphological matrix, 'Missing' and 'Not applicable' are considered invalid states. If a character has invalid states for the group being classified, it will be ignored.\n
                        6. States are represented by numbers. For example, '1 and 2' means multiple states should be treated as a single state type, and This multi-state characterization should not be confused with the individual states within it. The classification character should have no more than three state types.\n
                        7. I will use information gain to calculate all character and choose the highest inforamtion gain result, The higher the Information Gain result, the greater the contribution of the feature to the classification. \n
                        8. The final result will provide only the initial classification character and the categorization of species based on its state. \n
                        9. Don't need to show how the process about choose, only need to show the final result, and i will store result in #character classify result# block
                        Please provide the group morphological matrix data so that I can proceed with the classification.
                    """
             },
            {"role": "user", "content": f"Here is the group information need to be classify: '2': ['Equisetum_pratense', 'Equisetum_hyemale', 'Equisetum_moorei', 'Equisetum_ramosissimum', 'Equisetum_trachyodon', 'Equisetum_variegatum'], and here is the morpological matrix{json.dumps(data)}"}
        ]
    response =  client.chat.completions.create(
            model="gpt-4o",
            messages=messages,
            stop=None,
            temperature=0,
            max_tokens=1000,
            n = 1
    )
    result = response.choices[0].message.content
print(result)