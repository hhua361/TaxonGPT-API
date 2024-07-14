import json
import os
import re
import pandas as pd
from openai import OpenAI

class TaxonGPT:
    def __init__(self, api_key):
        self.api_key = api_key
        self.client = OpenAI(api_key=self.api_key)

    def load_prompt_messages(self, file_path):
        with open(file_path, "r", encoding="utf-8") as file:
            return json.load(file)

    def load_character_messages(self, file_path):
        with open(file_path, "r", encoding="utf-8") as file:
            return json.load(file)

    def letter_to_number(self, letter):
        return str(ord(letter) - ord('A') + 10)

    def parse_matrix(self, matrix_content):
        data = []
        headers = []
        lines = matrix_content.strip().split('\n')
        for i in range(0, len(lines), 2):
            taxa = lines[i].strip().strip("'")
            traits = lines[i + 1].strip()
            species_traits = []
            j = 0
            while j < len(traits):
                if traits[j] == '(':
                    j += 1
                    states = ''
                    while traits[j] != ')':
                        if traits[j].isalpha():
                            states += self.letter_to_number(traits[j])
                        else:
                            states += traits[j]
                        j += 1
                    species_traits.append(','.join(states))
                elif traits[j] == '?':
                    species_traits.append('Missing')
                elif traits[j] == '-':
                    species_traits.append('Not Applicable')
                elif traits[j].isalpha():
                    species_traits.append(self.letter_to_number(traits[j]))
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

    def convert_nexus_to_csv(self, nexus_file_path):
        try:
            encodings = ['utf-8', 'gbk', 'latin1']
            for encoding in encodings:
                try:
                    with open(nexus_file_path, 'r', encoding=encoding) as file:
                        content = file.read()
                    print(f"Successfully read file with encoding: {encoding}")
                    break
                except UnicodeDecodeError:
                    print(f"Failed to read file with encoding: {encoding}")
                    continue
            else:
                raise ValueError("Failed to read file with all attempted encodings.")
            matrix_content = re.search(r'MATRIX\s*(.*?)\s*;', content, re.DOTALL).group(1).strip()
            df = self.parse_matrix(matrix_content)
            df.to_csv("output.csv", index=False)
            return df
        except FileNotFoundError:
            print(f"File {nexus_file_path} not found.")
        except Exception as e:
            print(f"Error: {e}")

    def build_knowledge_graph(self, matrix):
        knowledge_graph = {}
        for _, row in matrix.iterrows():
            taxa = row.iloc[0]
            characteristics = {}
            for col in matrix.columns[1:]:
                state = row[col]
                if isinstance(state, str) and ',' in state:
                    state = state.replace(',', ' and ')
                characteristics[col] = str(state)
            knowledge_graph[taxa] = {'Characteristics': characteristics}
        self.knowledge_graph = knowledge_graph

    def save_knowledge_graph_as_json(self):
        with open("knowledge_graph.json", 'w') as f:
            json.dump(self.knowledge_graph, f, indent=4)

    def initial_classification(self, prompt_messages):
        content_with_data = prompt_messages["initial_character_messages"][3]["content_template"].format(
            knowledge_graph=json.dumps(self.knowledge_graph)
        )
        messages_initial = [
            prompt_messages["initial_character_messages"][0],
            prompt_messages["initial_character_messages"][1],
            prompt_messages["initial_character_messages"][2],
            {"role": "user", "content": content_with_data},
        ]
        initial_character_info = self.client.chat.completions.create(
            model="gpt-4o",
            messages=messages_initial,
            stop=None,
            max_tokens=1000,
            temperature=0,
            n=1
        )
        self.initial_response = initial_character_info.choices[0].message.content
        print(self.initial_response)

    def parse_classification_result(self, result_text):
        classification = {"Character": None, "States": {}}
        try:
            character_match = re.search(r'"Character": "([^"]+)"', result_text)
            if character_match:
                classification["Character"] = character_match.group(1)
            else:
                raise ValueError("Character not found in the result text.")
            state_sections = re.findall(r'"(\d+|[^"]+)":\s*\[(.*?)\]', result_text)
            if not state_sections:
                raise ValueError("No states found in the result text.")
            for state, species_block in state_sections:
                species_list = re.findall(r'"([^"]+)"', species_block)
                if not species_list:
                    raise ValueError(f"No species found for state {state}.")
                classification["States"][state] = species_list
        except Exception as e:
            print(f"Error parsing classification result: {e}")
            raise e
        return classification

    def generate_groups_from_classification(self, classification_result):
        groups = []
        for state, species_list in classification_result["States"].items():
            groups.append((state, species_list))
        return groups

    def extract_json_string(self, json_string):
        start = json_string.find('{')
        end = json_string.rfind('}') + 1
        if start != -1 and end != -1:
            cleaned_string = json_string[start:end]
            return cleaned_string.strip()
        return ""

    def recursive_classification(self, groups, depth=0, max_depth=10):
        state, current_group = None, []
        while groups:
            try:
                state, current_group = groups.pop(0)
                print(f"Processing group with state: {state}, species: {current_group}, at depth: {depth}")
                if len(current_group) == 1:
                    self.final_classification[current_group[0]] = current_group
                elif depth >= max_depth:
                    print(f"Reached max depth {max_depth}. Stopping further classification for group: {current_group}")
                    self.final_classification[state] = current_group
                else:
                    classification_result = self.classify_group(current_group)
                    cleaned_classification_result = self.extract_json_string(classification_result)
                    self.classification_results[state] = cleaned_classification_result
                    parsed_result = self.parse_classification_result(classification_result)
                    new_groups = self.generate_groups_from_classification(parsed_result)
                    self.recursive_classification(new_groups, depth + 1, max_depth)
            except Exception as e:
                print(f"Error processing group with state: {state}, species: {current_group}, at depth: {depth}")
                print(f"Exception: {e}")
                raise e
        return self.final_classification

    def classify_group(self, group_species):
        group_matrix = {species: self.knowledge_graph[species] for species in group_species}
        group_matrix_str = json.dumps(group_matrix, ensure_ascii=False)
        content_with_data = self.prompt_messages["secondary_character_messages"][3]["content_template"].format(
            group_matrix_str=group_matrix_str
        )
        messages_secondary = [
            self.prompt_messages["secondary_character_messages"][0],
            self.prompt_messages["secondary_character_messages"][1],
            self.prompt_messages["secondary_character_messages"][2],
            {"role": "user", "content": content_with_data},
        ]
        response = self.client.chat.completions.create(
            model="gpt-4o",
            messages=messages_secondary,
            stop=None,
            temperature=0,
            max_tokens=1000,
            n=1
        )
        result_secondary = response.choices[0].message.content
        content_with_data = self.prompt_messages["JSON_format_messages"][3]["content_template"].format(
            result_secondary=result_secondary
        )
        messages_JSON1 = [
            self.prompt_messages["JSON_format_messages"][0],
            self.prompt_messages["JSON_format_messages"][1],
            self.prompt_messages["JSON_format_messages"][2],
            {"role": "user", "content": content_with_data}
        ]
        response = self.client.chat.completions.create(
            model="gpt-4o",
            messages=messages_JSON1,
            stop=None,
            temperature=0,
            max_tokens=1500,
            n=1
        )
        json_result = response.choices[0].message.content
        print(json_result)
        return json_result

    def validate_results(self):
        errors = []
        for key, results in self.final_classification.items():
            for species, data in results.items():
                if species in self.knowledge_graph:
                    mismatch = False
                    incorrect_character_states = {}
                    for character, state in data["Characteristics"].items():
                        character = character.replace(" ", "").strip()
                        correct_state = self.knowledge_graph[species]["Characteristics"].get(character)
                        if correct_state is None or not self.check_state_match(state, correct_state):
                            mismatch = True
                            incorrect_character_states[character] = {"error_state": state, "correct_state": correct_state}
                    if mismatch:
                        errors.append({
                            "species": species,
                            "key": key,
                            "error": "Mismatch",
                            "error_result": incorrect_character_states,
                            "correct_result": {character: self.knowledge_graph[species]["Characteristics"].get(character) for character in incorrect_character_states}
                        })
                else:
                    errors.append({
                        "species": species,
                        "key": key,
                        "error": "Species not found in knowledge graph",
                        "error_result": data["Characteristics"]
                    })
        return errors

    def check_state_match(self, state, correct_state):
        if correct_state is None:
            return False
        if " and " in correct_state:
            correct_states = correct_state.split(" and ")
            return all(sub_state in correct_states for sub_state in state.split(" and "))
        return state == correct_state

    def correct_classification(self, errors):
        for error in errors:
            key = error['key']
            species_list = self.get_species_list_for_state(key)
            if not species_list:
                continue
            group_matrix = {s: self.knowledge_graph[s] for s in species_list}
            group_matrix_str = json.dumps(group_matrix, ensure_ascii=False)
            content_error = self.prompt_messages["correct_messages"][2]["content_template"].format(error=error)
            content_group_matrix = self.prompt_messages["correct_messages"][4]["content_template"].format(group_matrix_str=group_matrix_str)
            messages_correct = [
                self.prompt_messages["correct_messages"][0],
                self.prompt_messages["correct_messages"][1],
                {"role": "user", "content": content_error},
                self.prompt_messages["correct_messages"][3],
                {"role": "user", "content": content_group_matrix}
            ]
            response = self.client.chat.completions.create(
                model="gpt-4o",
                messages=messages_correct,
                stop=None,
                temperature=0,
                max_tokens=1000,
                n=1
            )
            corrected_result = response.choices[0].message.content
            content_with_data = self.prompt_messages["JSON_format_messages"][3]["content_template"].format(
                result_secondary=corrected_result
            )
            messages_JSON2 = [
                self.prompt_messages["JSON_format_messages"][0],
                self.prompt_messages["JSON_format_messages"][1],
                self.prompt_messages["JSON_format_messages"][2],
                {"role": "user", "content": content_with_data}
            ]
            response = self.client.chat.completions.create(
                model="gpt-4o",
                messages=messages_JSON2,
                stop=None,
                temperature=0,
                max_tokens=1500,
                n=1
            )
            json_result = response.choices[0].message.content
            json_cleaned_result = self.extract_json_string(json_result)
            print(json_cleaned_result)
            self.classification_results[key] = json_cleaned_result

    def get_species_list_for_state(self, key):
        species_list = []
        for state, species in self.groups:
            if state == key:
                species_list = species
                break
        if not species_list:
            print(f"Key {key} not found in groups")
        else:
            print(f"Processing species list for state '{key}': {species_list}")
        return species_list

    def extract_paths(self, node, path=None):
        if path is None:
            path = {}
        if 'Character' in node and 'States' in node:
            current_character = node['Character'].replace(" ", "").strip()
            for state, value in node['States'].items():
                new_path = path.copy()
                new_path[current_character] = state
                if isinstance(value, dict):
                    yield from self.extract_paths(value, new_path)
                else:
                    for species in value:
                        yield species, new_path

    def process_final_classification(self):
        self.final_results = {}
        for key, json_str in self.classification_results.items():
            classification_data = json.loads(json_str)
            species_paths = list(self.extract_paths(classification_data))
            formatted_results = {}
            for species, path in species_paths:
                formatted_results[species] = {"Characteristics": path}
            self.final_results[key] = formatted_results

    def replace_indices_with_descriptions_in_key(self, key, character_info, parent_char_index=None):
        updated_key = {}
        for char_state, subtree in key.items():
            if char_state.startswith("Character"):
                parts = char_state.split()
                if len(parts) > 1:
                    char_index = parts[1]
                    if char_index in character_info:
                        char_description = f"Character {char_index}: {character_info[char_index]['description']}"
                        if isinstance(subtree, dict):
                            updated_subtree = self.replace_indices_with_descriptions_in_key(subtree, character_info, char_index)
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
                state_key = f"State {' '.join(states)}: {';'.join(state_descriptions)}"
                if isinstance(subtree, dict):
                    updated_key[state_key] = self.replace_indices_with_descriptions_in_key(subtree, character_info, parent_char_index)
                else:
                    updated_key[state_key] = subtree
            else:
                updated_key[char_state] = subtree
        return updated_key

    def convert_structure(self, node):
        if "Character" in node and "States" in node:
            character = node["Character"]
            states = node["States"]
            converted = {f"Character {character.replace('Character', '')}": {}}
            for state, sub_node in states.items():
                state_key = f"State {state}"
                if isinstance(sub_node, list):
                    converted[f"Character {character.replace('Character', '')}"][state_key] = sub_node[0] if len(sub_node) == 1 else sub_node
                elif isinstance(sub_node, dict):
                    converted[f"Character {character.replace('Character', '')}"][state_key] = self.convert_structure(sub_node)
            return converted
        return node

    def combine_results(self, initial, secondary, state_key):
        if not secondary:
            return
        initial_states = initial["States"].get(state_key)
        if initial_states is None:
            initial["States"][state_key] = secondary
            return
        if isinstance(initial_states, list):
            if isinstance(secondary, list):
                initial["States"][state_key] = list(set(initial_states + secondary))
            else:
                initial["States"][state_key] = secondary
        elif isinstance(initial_states, dict):
            if isinstance(secondary, dict):
                for key, value in secondary["States"].items():
                    if key not in initial_states:
                        initial_states[key] = value
                    else:
                        self.combine_results(initial_states, value, key)
            else:
                raise ValueError(f"Conflicting types for key {state_key}: {type(initial_states)} vs {type(secondary)}")
        else:
            raise ValueError(f"Unexpected type for initial states: {type(initial_states)}")

    def generate_classification_key(self, data, current_step, parent_step=None):
        global step_counter
        if isinstance(data, dict):
            state_steps = []
            step_map = {}
            for character, states in data.items():
                for state, next_level in states.items():
                    full_state_description = f"{character.split(':')[1]}: {state.split(': ')[1]}"
                    if isinstance(next_level, dict):
                        step_counter += 1
                        next_step_prefix = str(step_counter)
                        state_steps.append(f"    - {full_state_description} ........ {next_step_prefix}")
                        step_map[step_counter] = (next_level, current_step)
                    else:
                        state_steps.append(f"    - {full_state_description} ........ {next_level}")
            if parent_step:
                self.steps.append(f"{current_step}({parent_step}).")
            else:
                self.steps.append(f"{current_step}.")
            self.steps.extend(state_steps)
            for step, (next_level, parent_step) in step_map.items():
                self.generate_classification_key(next_level, step, parent_step)
        else:
            return

    def process_key(self, nexus_file_path, prompt_file_path, character_file_path):
        self.prompt_messages = self.load_prompt_messages(prompt_file_path)
        self.character_info = self.load_character_messages(character_file_path)

        df = self.convert_nexus_to_csv(nexus_file_path)
        self.build_knowledge_graph(df)
        self.save_knowledge_graph_as_json()
        self.initial_classification(self.prompt_messages)
        parsed_initial_classification = self.parse_classification_result(self.initial_response)
        self.groups = self.generate_groups_from_classification(parsed_initial_classification)
        self.final_classification = self.recursive_classification(self.groups)
        errors = self.validate_results()
        while errors:
            self.correct_classification(errors)
            self.final_classification = {}
            self.process_final_classification()
            errors = self.validate_results()
        self.save_final_classification()

        self.steps = []
        step_counter = 1
        self.generate_classification_key(self.updated_classification_key, 1)
        classification_key = "\n".join(self.steps)
        print(classification_key)
        with open("classification_key.txt", "w") as f:
            f.write(classification_key)

    def generate_taxonomic_description(self, species_name, species_data, character_info, prompt_messages):
        content_with_data = prompt_messages["description_messages"][3]["content_template"].format(
            species_name=species_name,
            species_data=json.dumps(species_data),
            character_info=json.dumps(character_info)
        )
        messages = [
            prompt_messages["description_messages"][0],
            prompt_messages["description_messages"][1],
            prompt_messages["description_messages"][2],
            {"role": "user", "content": content_with_data},
            prompt_messages["description_messages"][4]
        ]
        response = self.client.chat.completions.create(
            model="gpt-4o",
            messages=messages,
            stop=None,
            temperature=0,
            n=1
        )
        result = response.choices[0].message.content
        return result

    def process_description(self, matrix_file_path, character_info_file_path, output_file_path, prompt_file_path):
        with open(matrix_file_path, "r", encoding="utf-8") as file:
            matrix_data = json.load(file)

        with open(character_info_file_path, "r", encoding="utf-8") as file:
            character_info = json.load(file)

        prompt_messages = self.load_prompt_messages(prompt_file_path)

        taxonomic_descriptions = {}
        for species_name, species_data in matrix_data.items():
            description = self.generate_taxonomic_description(species_name, species_data, character_info, prompt_messages)
            taxonomic_descriptions[species_name] = description

        with open(output_file_path, 'w', encoding='utf-8') as f:
            json.dump(taxonomic_descriptions, f, ensure_ascii=False, indent=4)

        print(f"Taxonomic descriptions have been generated and saved to '{output_file_path}'.")

# Example usage
api_key = os.getenv("OPENAI_API_KEY")

# Generate Taxonomic Key
nexus_file_path = "D:/桌面/taxonomy_primary_result/The_GPT-4_result/Dataset_11 (grass genera) 19/Information gain methods/grass.nex"
prompt_file_path = "D:/桌面/taxonomy_primary_result/Taxonomic dataset materials/prompt_messages.json"
character_file_path = "D:/桌面/taxonomy_primary_result/The_GPT-4_result/Dataset_11 (grass genera) 19/Information gain methods/character_info_update.json"

taxon_gpt = TaxonGPT(api_key)
taxon_gpt.process_key(nexus_file_path, prompt_file_path, character_file_path)

# Generate Taxonomic Descriptions
matrix_file_path = "D:/桌面/TEST-KG/nexus fix/matrix_knowledge_graph_22.json"
character_info_file_path = "D:/桌面/TEST-KG/nexus fix/updated_character_info.json"
output_file_path = "D:/桌面/taxonomic_descriptions.json"

taxon_gpt.process_description(matrix_file_path, character_info_file_path, output_file_path, prompt_file_path)
