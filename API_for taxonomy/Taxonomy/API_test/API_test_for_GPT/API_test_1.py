import pandas as pd
import re
import json

def letter_to_number(letter):
    return str(ord(letter) - ord('A') + 10)

def parse_matrix(matrix_content):
    data = []
    headers = []

    lines = matrix_content.strip().split('\n')
    for i in range(0, len(lines), 2):
        if i + 1 >= len(lines):
            raise ValueError("Matrix format error: Each taxa should be followed by its traits on the next line.")
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
    df = pd.DataFrame(data, columns=headers)

    return df


def convert_nexus_to_csv(matrix_content, output_path):
    df = parse_matrix(matrix_content)
    df.to_csv(output_path, index=False)


def parse_charstatelabels(charstatelabels_content):
    charlabels = {}
    statelabels = {}
    char_pattern = re.compile(r"(\d+)\s+(.+?)\s*/\s*(.+)")

    for line in charstatelabels_content.strip().split('\n'):
        match = char_pattern.match(line.strip())
        if match:
            char_index = int(match.group(1))
            char_description = match.group(2).strip()
            states_content = match.group(3).strip()
            states = [state.strip().strip("'") for state in states_content.split()]
            charlabels[char_index] = char_description
            statelabels[char_index] = states

    return charlabels, statelabels


def parse_nexus_file(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        content = file.read()

    charstatelabels_match = re.search(r'CHARSTATELABELS\s*(.*?)\s*MATRIX', content, re.DOTALL)
    if not charstatelabels_match:
        raise ValueError("CHARSTATELABELS section not found in the Nexus file.")
    charstatelabels_content = charstatelabels_match.group(1)

    matrix_match = re.search(r'MATRIX\s*(.*?)\s*;', content, re.DOTALL)
    if not matrix_match:
        raise ValueError("MATRIX section not found in the Nexus file.")
    matrix_content = matrix_match.group(1).strip()

    charlabels, statelabels = parse_charstatelabels(charstatelabels_content)

    return charlabels, statelabels, matrix_content


def convert_to_knowledge_graph(charlabels, statelabels):
    knowledge_graph = {"characters": []}
    for char_index, description in charlabels.items():
        states = statelabels.get(char_index, [])
        state_dict = {i + 1: state for i, state in enumerate(states)}
        character_info = {
            "id": char_index,
            "description": description,
            "states": state_dict
        }
        knowledge_graph["characters"].append(character_info)

    return knowledge_graph


def convert_nexus_to_json(charlabels, statelabels, output_path):
    knowledge_graph = convert_to_knowledge_graph(charlabels, statelabels)
    with open(output_path, "w", encoding='utf-8') as f:
        json.dump(knowledge_graph, f, indent=4)


def convert_csv_to_knowledge_graph(csv_file_path, output_json_path):
    df = pd.read_csv(csv_file_path)
    knowledge_graph = {"taxa": []}

    for _, row in df.iterrows():
        taxa_info = {"taxa": row['taxa'], "characters": {}}
        for col in df.columns[1:]:
            states = row[col]
            if isinstance(states, str) and ',' in states:
                states = states.split(',')
            taxa_info["characters"][col] = states
        knowledge_graph["taxa"].append(taxa_info)

    with open(output_json_path, "w", encoding='utf-8') as f:
        json.dump(knowledge_graph, f, indent=4)


if __name__ == "__main__":
    nexus_file_path = "D:/桌面/taxonomy_primary_result/The_GPT-4_result/Dataset_12 (Translating Niphargus barcodes from Switzerland into taxonomy with a description of two new species (Amphipoda, Niphargidae) ) 20/Information gain methods/nexdata-1"
    csv_output_path = "D:/桌面/taxonomy_primary_result/The_GPT-4_result/test/processed_matrix.csv"
    charstate_json_output_path = "D:/桌面/taxonomy_primary_result/The_GPT-4_result/test/charstate_knowledge_graph.json"
    matrix_json_output_path = "D:/桌面/taxonomy_primary_result/The_GPT-4_result/test/matrix_knowledge_graph.json"

    try:
        # 解析Nexus文件
        charlabels, statelabels, matrix_content = parse_nexus_file(nexus_file_path)

        # Part 1: 转换Nexus文件为CSV
        convert_nexus_to_csv(matrix_content, csv_output_path)

        # Part 2: 提取character和state信息并转换为JSON
        convert_nexus_to_json(charlabels, statelabels, charstate_json_output_path)

        # Part 3: 转换CSV文件为JSON
        convert_csv_to_knowledge_graph(csv_output_path, matrix_json_output_path)

        # 打印结果
        with open(charstate_json_output_path, 'r', encoding='utf-8') as f:
            charstate_json = json.load(f)
            print(json.dumps(charstate_json, indent=4))

        with open(matrix_json_output_path, 'r', encoding='utf-8') as f:
            matrix_json = json.load(f)
            print(json.dumps(matrix_json, indent=4))
    except ValueError as e:
        print(e)

"""
nexus_file_path = "D:/桌面/taxonomy_primary_result/The_GPT-4_result/Dataset_12 (Translating Niphargus barcodes from Switzerland into taxonomy with a description of two new species (Amphipoda, Niphargidae) ) 20/Information gain methods/nexdata-1"
    csv_output_path = "D:/桌面/taxonomy_primary_result/The_GPT-4_result/test/processed_matrix.csv"
    charstate_json_output_path = "D:/桌面/taxonomy_primary_result/The_GPT-4_result/test/charstate_knowledge_graph.json"
    matrix_json_output_path = "D:/桌面/taxonomy_primary_result/The_GPT-4_result/test/matrix_knowledge_graph.json"
"""