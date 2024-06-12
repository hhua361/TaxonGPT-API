import pandas as pd
import re
import os
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
        with open(file_path, 'r') as file:
            content = file.read()
        matrix_content = re.search(r'MATRIX\s*(.*?)\s*;', content, re.DOTALL).group(1).strip()
        df = parse_matrix(matrix_content)
        df.to_csv(output_path, index=False)
    except FileNotFoundError:
        print(f"File {file_path} not found.")
    except Exception as e:
        print(f"Appear error：{e}")

file_path = "D:/桌面/taxonomy_primary_result/The_GPT-4_result/Dataset_2 (The Equisetum species (horsetails)) 3/Information gain methods/nexdata"
output_path = "D:/桌面/taxonomy_primary_result/The_GPT-4_result/Dataset_2 (The Equisetum species (horsetails)) 3/Information gain methods/process_data_2.csv"
csv_matrix = convert_nexus_to_csv(file_path, output_path)
processed_df = pd.read_csv(output_path)