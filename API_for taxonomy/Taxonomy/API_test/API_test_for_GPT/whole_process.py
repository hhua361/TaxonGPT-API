# all package
import pandas as pd
import re
import json
from openai import OpenAI
import os
import argparse


client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
model_use = "gpt-3.5-turbo"

### Part 1：部分是关于将导入的Nexus信息中的矩阵信息提取出来，转换为csv文件
### 这个部分主要是关于将Nexus矩阵的信息转化为csv这种结构化类型的数据

def letter_to_number(letter):
    return str(ord(letter) - ord('A') + 10)
def parse_matrix(matrix_content):
    data = []
    headers = []
    lines = matrix_content.strip().split('\n')
    for i in range(0, len(lines), 2):
        taxa = lines[i].strip("'").strip()
        traits = lines[i + 1].strip()
        species_traits = []
        j = 0
        while j < len(traits):
            if traits[j] == '(':
                j += 1
                states = ''
                while traits[j] != ')':
                    if traits[j].isalpha():
                        states += letter_to_number(traits[j])
                    else:
                        states += traits[j]
                    j += 1
                species_traits.append(','.join(states))
            elif traits[j] == '?':
                species_traits.append('Missing')
            elif traits[j] == '-':
                species_traits.append('Not Applicable')
            elif traits[j].isalpha():
                species_traits.append(letter_to_number(traits[j]))
            else:
                species_traits.append(traits[j])
            j += 1
        data.append([taxa] + species_traits)
    max_traits = max(len(row) - 1 for row in data)
    headers = ['taxa'] + [f'Character{i + 1}' for i in range(max_traits)]
    try:
        df = pd.DataFrame(data, columns=headers)
        return df
    except Exception as e:
        print(f"Error creating DataFrame: {e}")
        return None
def convert_nexus_to_csv(file_path, output_path):
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            content = file.read()
        matrix_content = re.search(r'MATRIX\s*(.*?)\s*;', content, re.DOTALL).group(1).strip()
        df = parse_matrix(matrix_content)
        df.to_csv(output_path, index=False)
    except FileNotFoundError:
        print(f"File {file_path} not found.")
    except Exception as e:
        print(f"Appear error：{e}")

file_path = "D:/桌面/taxonomy_primary_result/The_GPT-4_result/Dataset_12 (Translating Niphargus barcodes from Switzerland into taxonomy with a description of two new species (Amphipoda, Niphargidae) ) 20/Information gain methods/nexdata"
output_path = "D:/桌面/taxonomy_primary_result/The_GPT-4_result/Dataset_12 (Translating Niphargus barcodes from Switzerland into taxonomy with a description of two new species (Amphipoda, Niphargidae) ) 20/Information gain methods/process_data.csv"
csv_matrix = convert_nexus_to_csv(file_path, output_path)
processed_df = pd.read_csv(output_path)
# print(processed_df.head())


# part 2：是通过使用code将Nexus中的characterlabel提取出来知道每个character和状态所对应的数字
def read_nexus_file(file_path):
    with open(file_path, 'r') as file:
        content = file.read()
    return content
def extract_section(content, section_name):
    pattern = re.compile(rf'{section_name}\n(.*?);', re.DOTALL | re.MULTILINE)
    match = pattern.search(content)
    if match:
        return match.group(1).strip()
    return None
def parse_charlabels(charlabels_content):
    charlabels = {}
    lines = charlabels_content.strip().split("\n")
    char_pattern = re.compile(r"\[(\d+)\(\d+\)\]\s+'(.+?)'")
    for line in lines:
        match = char_pattern.match(line.strip().rstrip(','))
        if match:
            char_index = int(match.group(1))
            description = match.group(2)
            charlabels[char_index] = description
    return charlabels
def parse_statelabels(statelabels_content):
    statelabels = {}
    lines = statelabels_content.strip().split("\n")
    current_char = None
    states = []
    for line in lines:
        line = line.strip().rstrip(',')
        if re.match(r'^\d+', line):
            if current_char is not None:
                statelabels[current_char] = states
            parts = line.split(' ', 1)
            current_char = int(parts[0])
            states = parts[1].strip().split("' '")
            states = [state.strip("'") for state in states if state != ';']
        else:
            additional_states = line.split("' '")
            additional_states = [state.strip("'") for state in additional_states if state != ';']
            states.extend(additional_states)

    if current_char is not None:
        statelabels[current_char] = states
    return statelabels
def combine_labels_and_states(charlabels, statelabels):
    character_info = {}
    for char_index, description in charlabels.items():
        states = statelabels.get(char_index, [])
        state_dict = {i + 1: state for i, state in enumerate(states)}
        character_info[char_index] = {
            "description": description,
            "states": state_dict
        }
    return character_info
file_path = "D:/桌面/taxonomy_primary_result/The_GPT-4_result/Dataset_12 (Translating Niphargus barcodes from Switzerland into taxonomy with a description of two new species (Amphipoda, Niphargidae) ) 20/DELTA_data/nexdata"
nexus_content = read_nexus_file(file_path)
charlabels_content = extract_section(nexus_content, "CHARLABELS")
statelabels_content = extract_section(nexus_content, "STATELABELS")
if charlabels_content and statelabels_content:
    charlabels = parse_charlabels(charlabels_content)
    statelabels = parse_statelabels(statelabels_content)
    character_info = combine_labels_and_states(charlabels, statelabels)
    print(json.dumps(character_info, indent=4))
    output_path = "D:/桌面/taxonomy_primary_result/The_GPT-4_result/Dataset_12 (Translating Niphargus barcodes from Switzerland into taxonomy with a description of two new species (Amphipoda, Niphargidae) ) 20/character_info.json"
    with open(output_path, "w") as f:
        json.dump(character_info, f, indent=4)
else:
    print("Failure to extract to CHARLABELS or STATELABELS section")


# part 3：是通过将已经生成的csv文件转化为knowledge graph的JSON格式
def read_nexus_matrix(file_path):
    df = pd.read_csv(file_path)
    return df
def build_knowledge_graph(matrix):
    knowledge_graph = {}
    for _, row in matrix.iterrows():
        taxa = row.iloc[0]
        characteristics = {}
        for col in matrix.columns[1:]:
            state = row[col]
            if isinstance(state, str) and ',' in state:
                state = state.replace(',', ' and ')
            characteristics[col] = str(state)
        knowledge_graph[taxa] = {
            'Characteristics': characteristics
        }
    return knowledge_graph
def save_knowledge_graph_as_json(knowledge_graph, file_path):
    with open(file_path, 'w') as f:
        json.dump(knowledge_graph, f, indent=4)

file_path = "D:/桌面/taxonomy_primary_result/The_GPT-4_result/Dataset_12 (Translating Niphargus barcodes from Switzerland into taxonomy with a description of two new species (Amphipoda, Niphargidae) ) 20/Information gain methods/process_data.csv"
nexus_matrix = read_nexus_matrix(file_path)
knowledge_graph = build_knowledge_graph(nexus_matrix)
save_file_path = "D:/桌面/taxonomy_primary_result/The_GPT-4_result/Dataset_12 (Translating Niphargus barcodes from Switzerland into taxonomy with a description of two new species (Amphipoda, Niphargidae) ) 20/matrix_knowledge_graph.json"
save_knowledge_graph_as_json(knowledge_graph, save_file_path)
knowledge_graph_json = json.dumps(knowledge_graph, indent=4)
#print(knowledge_graph_json)

# part 4：设置一个存储prompt的部分，通过对不同部分进行处理，来选择不同的prompt部分
# part 5：设置关于API调用的函数
def generate_taxonomic_key(csv_matrix):  # ,max_tokens,temperature
    global model_use
    # Message sequence for coding morphological characteristics
    messages = [
        {"role": "system","content": "You are a helpful taxonomic assistant, skilled in calculate the information gain and building taxonomic key."},
        {"role": "user","content": "Generation of Taxonomic key from Morphological Matrix"},
        {"role": "user","content": "I need to generate a taxonomic key using a morphological matrix provided in a CSV file. This matrix contains character states for various taxa. The goal is to determine the characters that best separate the taxa based on their states and progressively categorize them to construct the taxonomic key. The analysis should use information gain to evaluate each character's ability to classify the taxa evenly"},
        {"role": "user","content": "Please follow these requirements during the analysis:"},
        {"role": "user","content": "1, Initial Character Selection: Ensure all taxa have a defined state ('Missing' or 'Not applicable' is an invalid status) for the first character. Ignore characters with more than two states type and use information gain to select the most suitable character for initial classification."},
        {"role": "user","content": "2, Dynamic Character Selection: For each new character selection, reload the original matrix. Re-evaluate the presence of invalid states in character, Ignore characters with missing or not applicable states for the current subset of taxa. Include characters with actual states for the taxa being considered, even if they have missing or not applicable states for other taxa."},
        {"role": "user","content": "3, Character Selection Preference: Prefer characters with fewer state types when multiple characters have the same information gain. Ignore characters with more than three state types regardless of their information gain."},
        {"role": "user","content": "4, Step-by-Step Classification: Classify taxa step-by-step according to the above rules until all taxa are individually classified. Display the results in a nested structure without showing the code implementation."},
        {"role": "assistant", "content": "Sure, I can help with that. Please provide the csv file."},
        {"role": "user", "content": csv_matrix},
    ]
    response = client.chat.completions.create(model=model_use,
                                              messages=messages,
                                              max_tokens=1600,
                                              temperature=0.3,
                                              stop=None)
    return response.choices[0].message.content

def character_mapping_for_taxonomic_key(taxonomic_key):
    global model_use
    # Message sequence for coding morphological characteristics
    messages = [
        {"role": "system","content": "You are a helpful taxonomic assistant, skilled in building taxonomic key and character mapping."},
        {"role": "user", "content": "After generating the taxonomic key, need to add the corresponding CHARACTER and STATE information"},
        {"role": "user","content": "perform character mapping, based on the corresponding CHARACTER's STATE that is provided to you"},
        {"role": "assistant", "content": "Sure, I can help with that. Please provide the character and state information."},
        {"role": "user", "content": character_info},
        {"role": "user","content": "where ',' is used to indicate that more than one state exists at the same time for the same CHARACTER"},
        {"role": "user","content": "(such as the character1 1,2 means both this taxa for the character 1 both have state 1 and state 2)"},
        {"role": "user","content": "Finally keep the numerical labeling"},
        {"role": "user", "content": csv_matrix},
    ]
    response = client.chat.completions.create(model=model_use,
                                              messages=messages,
                                              max_tokens=1600,
                                              temperature=0.3,
                                              stop=None)
    return response.choices[0].message.content

def generatet_taxonomic_description(knowledge_graph):
    global model_use
    # Message sequence for coding morphological characteristics
    messages = [
        {"role": "system","content": "Generation of Taxonomic Descriptions from Morphological Matrix"},
        {"role": "user", "content": "Based on the provided morphological matrix (presented as a knowledge graph in JSON format), standard taxonomic descriptions are generated for all taxa in the matrix."},
        {"role": "user","content": "Additional CHARACTER labels and STATE labels will be provided, these labels contain a detailed description of each CHARACTER and its corresponding STATE."},
        {"role": "user", "content": "Multiple states in the matrix (e.g., '1 and 2') indicate that the CHARACTER of that TAXA has both state 1 and state 2."},
        {"role": "user","content": "Specific requirements:"},
        {"role": "user","content": "1, Generate standard academic taxonomic descriptions, which need to include all characters in the morphological matrix and accurately correspond to the state of each character."},
        {"role": "user","content": "2, Generate descriptions in list form and paragraph form. In paragraph form, the number of each character should be indicated."},
        {"role": "user", "content": "Due to the large number of results, to avoid space constraints, please show the taxonomic description of each taxa separately."},
        {"role": "user", "content": knowledge_graph_json},
        {"role": "user", "content": character_info},
    ]
    response = client.chat.completions.create(model=model_use,
                                              messages=messages,
                                              max_tokens=1600,
                                              temperature=0.3,
                                              stop=None)
    return response.choices[0].message.content
# part 6：或许可以添加对最终的结果进行补充处理，来最终优化这个结果（可以通过考虑使用条件语句来实现）
    taxonomic_key = generate_taxonomic_key(csv_matrix)
    # Coded extracted features
    character_info_taxonomic_key = character_mapping_for_taxonomic_key(taxonomic_key)
    # Construct NEXUS file contents
    taxonomic_description = generatet_taxonomic_description(knowledge_graph,character_info)