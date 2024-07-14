import json
import os
import re
import pandas as pd
import logging
from openai import OpenAI


class TaxonGPT:
    def __init__(self, config_file):
        """
        Initialize the TaxonGPT class.

        Parameters:
        config_file (str): Path to the configuration file.
        """
        with open(config_file, 'r', encoding='utf-8') as file:
            config = json.load(file)

        self.api_key = config["api_key"]
        self.client = OpenAI(api_key=self.api_key)
        self.paths = config["paths"]
        logging.basicConfig(filename='taxon_gpt.log', level=logging.DEBUG,
                            format='%(asctime)s %(levelname)s:%(message)s')

    def load_prompt_messages(self, file_path):
        """
        Load prompt messages.

        Parameters:
        file_path (str): Path to the prompt messages file.

        Returns:
        dict: Content of the prompt messages.

        Exceptions:
        FileNotFoundError: If the file is not found.
        JSONDecodeError: If there is an error decoding the JSON file.
        """
        try:
            with open(file_path, "r", encoding="utf-8") as file:
                return json.load(file)
        except FileNotFoundError:
            logging.error(f"File not found: {file_path}")
            raise
        except json.JSONDecodeError:
            logging.error(f"Error decoding JSON from file: {file_path}")
            raise

    def load_character_messages(self, file_path):
        """
        Load character messages.

        Parameters:
        file_path (str): Path to the character messages file.

        Returns:
        dict: Content of the character messages.

        Exceptions:
        FileNotFoundError: If the file is not found.
        JSONDecodeError: If there is an error decoding the JSON file.
        """
        try:
            with open(file_path, "r", encoding="utf-8") as file:
                return json.load(file)
        except FileNotFoundError:
            logging.error(f"File not found: {file_path}")
            raise
        except json.JSONDecodeError:
            logging.error(f"Error decoding JSON from file: {file_path}")
            raise

    def letter_to_number(self, letter):
        """
        Convert a letter to a number.

        Parameters:
        letter (str): The letter to be converted.

        Returns:
        str: The corresponding number.
        """
        return str(ord(letter) - ord('A') + 10)

    def parse_matrix(self, matrix_content):
        """
        Parse matrix content.

        Parameters:
        matrix_content (str): Content of the matrix file.

        Returns:
        pd.DataFrame: Parsed data as a DataFrame.

        Exceptions:
        Exception: Any error that occurs during parsing.
        """
        data = []
        headers = []
        lines = matrix_content.strip().split('\n')
        try:
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
            df = pd.DataFrame(data, columns=headers)
        except Exception as e:
            logging.error(f"Error parsing matrix: {e}")
            raise
        return df

    def convert_nexus_to_csv(self, nexus_file_path):
        """
        Convert Nexus file to CSV.

        Parameters:
        nexus_file_path (str): Path to the Nexus file.

        Returns:
        pd.DataFrame: Parsed data as a DataFrame.

        Exceptions:
        FileNotFoundError: If the file is not found.
        UnicodeDecodeError: If there is an error decoding the file.
        ValueError: If the file cannot be read with any encoding.
        """
        try:
            encodings = ['utf-8', 'gbk', 'latin1']
            for encoding in encodings:
                try:
                    with open(nexus_file_path, 'r', encoding=encoding) as file:
                        content = file.read()
                    logging.info(f"Successfully read file with encoding: {encoding}")
                    break
                except UnicodeDecodeError:
                    logging.warning(f"Failed to read file with encoding: {encoding}")
                    continue
            else:
                raise ValueError("Failed to read file with all attempted encodings.")
            matrix_content = re.search(r'MATRIX\s*(.*?)\s*;', content, re.DOTALL).group(1).strip()
            df = self.parse_matrix(matrix_content)
            df.to_csv("output.csv", index=False)
            return df
        except FileNotFoundError:
            logging.error(f"File {nexus_file_path} not found.")
            raise
        except Exception as e:
            logging.error(f"Error converting Nexus to CSV: {e}")
            raise

    def build_knowledge_graph(self, matrix):
        """
        Build knowledge graph from matrix.

        Parameters:
        matrix (pd.DataFrame): DataFrame containing matrix data.

        Returns:
        None

        Exceptions:
        Exception: Any error that occurs during the building of the knowledge graph.
        """
        try:
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
        except Exception as e:
            logging.error(f"Error building knowledge graph: {e}")
            raise

    def save_knowledge_graph_as_json(self):
        """
        Save knowledge graph as JSON file.

        Returns:
        None

        Exceptions:
        Exception: Any error that occurs during saving the knowledge graph as JSON.
        """
        try:
            with open("knowledge_graph.json", 'w', encoding='utf-8') as f:
                json.dump(self.knowledge_graph, f, indent=4)
        except Exception as e:
            logging.error(f"Error saving knowledge graph as JSON: {e}")
            raise

    def initial_classification(self, prompt_messages):
        """
        Perform initial classification.

        Parameters:
        prompt_messages (dict): Dictionary containing prompt messages.

        Returns:
        None

        Exceptions:
        Exception: Any error that occurs during the initial classification.
        """
        try:
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
            logging.info(f"Initial classification response: {self.initial_response}")
        except Exception as e:
            logging.error(f"Error during initial classification: {e}")
            raise

    def parse_classification_result(self, result_text):
        """
        Parse classification result.

        Parameters:
        result_text (str): Classification result text.

        Returns:
        dict: Dictionary representation of the classification result.

        Exceptions:
        ValueError: If there is an error parsing the classification result.
        """
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
            logging.error(f"Error parsing classification result: {e}")
            raise e
        return classification

    def generate_groups_from_classification(self, classification_result):
        """
        Generate groups from classification result.

        Parameters:
        classification_result (dict): Dictionary representation of the classification result.

        Returns:
        list: List of groups, each group is a tuple (state, species_list).

        Exceptions:
        Exception: If there is an error generating groups from classification.
        """
        try:
            groups = []
            for state, species_list in classification_result["States"].items():
                groups.append((state, species_list))
            return groups
        except Exception as e:
            logging.error(f"Error generating groups from classification: {e}")
            raise

    def extract_json_string(self, json_string):
        """
        Extract JSON string.

        Parameters:
        json_string (str): String containing JSON data.

        Returns:
        str: Extracted clean JSON string.

        Exceptions:
        Exception: If there is an error during extraction.
        """
        try:
            start = json_string.find('{')
            end = json_string.rfind('}') + 1
            if start != -1 and end != -1:
                cleaned_string = json_string[start:end]
                return cleaned_string.strip()
            return ""
        except Exception as e:
            logging.error(f"Error extracting JSON string: {e}")
            raise

    def recursive_classification(self, groups, depth=0, max_depth=10):
        """
        Recursive classification.

        Parameters:
        groups (list): Groups to be classified.
        depth (int): Current recursion depth.
        max_depth (int): Maximum recursion depth.

        Returns:
        None

        Exceptions:
        Exception: Any error that occurs during recursive classification.
        """
        state, current_group = None, []
        while groups:
            try:
                state, current_group = groups.pop(0)
                logging.debug(f"Processing group with state: {state}, species: {current_group}, at depth: {depth}")
                if len(current_group) == 1:
                    self.final_classification[current_group[0]] = current_group
                elif depth >= max_depth:
                    logging.debug(f"Reached max depth {max_depth}. Stopping further classification for group: {current_group}")
                    self.final_classification[state] = current_group
                else:
                    classification_result = self.classify_group(current_group)
                    cleaned_classification_result = self.extract_json_string(classification_result)
                    self.classification_results[state] = cleaned_classification_result
                    parsed_result = self.parse_classification_result(classification_result)
                    new_groups = self.generate_groups_from_classification(parsed_result)
                    self.recursive_classification(new_groups, depth + 1, max_depth)
            except Exception as e:
                logging.error(f"Error processing group with state: {state}, species: {current_group}, at depth: {depth}")
                raise e
        return self.final_classification

    def classify_group(self, group_species):
        """
        Classify a group of species.

        Parameters:
        group_species (list): List of species in the group.

        Returns:
        str: Classification result in JSON format.

        Exceptions:
        Exception: Any error that occurs during classification.
        """
        try:
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
            logging.info(f"Classification result: {json_result}")
            return json_result
        except Exception as e:
            logging.error(f"Error classifying group: {e}")
            raise

    def validate_results(self):
        """
        Validate classification results.

        Returns:
        list: List of errors found during validation.

        Exceptions:
        Exception: Any error that occurs during validation.
        """
        errors = []
        try:
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
        except Exception as e:
            logging.error(f"Error validating results: {e}")
            raise

    def check_state_match(self, state, correct_state):
        """
        Check if the state matches the correct state.

        Parameters:
        state (str): The state to be checked.
        correct_state (str): The correct state to match against.

        Returns:
        bool: True if the state matches the correct state, False otherwise.

        Exceptions:
        Exception: Any error that occurs during state matching.
        """
        try:
            if correct_state is None:
                return False
            if " and " in correct_state:
                correct_states = correct_state.split(" and ")
                return all(sub_state in correct_states for sub_state in state.split(" and "))
            return state == correct_state
        except Exception as e:
            logging.error(f"Error checking state match: {e}")
            raise

    def correct_classification(self, errors):
        """
        Correct classification based on errors.

        Parameters:
        errors (list): List of errors found during validation.

        Returns:
        None

        Exceptions:
        Exception: Any error that occurs during correction.
        """
        try:
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
                logging.info(f"Corrected classification result: {json_cleaned_result}")
                self.classification_results[key] = json_cleaned_result
        except Exception as e:
            logging.error(f"Error correcting classification: {e}")
            raise

    def get_species_list_for_state(self, key):
        """
        Get species list for a given state key.

        Parameters:
        key (str): The state key.

        Returns:
        list: List of species for the given state key.

        Exceptions:
        Exception: Any error that occurs during retrieval.
        """
        try:
            species_list = []
            for state, species in self.groups:
                if state == key:
                    species_list = species
                    break
            if not species_list:
                logging.warning(f"Key {key} not found in groups")
            else:
                logging.info(f"Processing species list for state '{key}': {species_list}")
            return species_list
        except Exception as e:
            logging.error(f"Error getting species list for state {key}: {e}")
            raise

    def extract_paths(self, node, path=None):
        """
        Extract paths from a classification node.

        Parameters:
        node (dict): The classification node.
        path (dict): The current path (used for recursion).

        Yields:
        tuple: Species and path.

        Exceptions:
        Exception: Any error that occurs during extraction.
        """
        try:
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
        except Exception as e:
            logging.error(f"Error extracting paths from node: {e}")
            raise

    def process_final_classification(self):
        """
        Process final classification.

        Returns:
        None

        Exceptions:
        Exception: Any error that occurs during processing.
        """
        try:
            self.final_results = {}
            for key, json_str in self.classification_results.items():
                classification_data = json.loads(json_str)
                species_paths = list(self.extract_paths(classification_data))
                formatted_results = {}
                for species, path in species_paths:
                    formatted_results[species] = {"Characteristics": path}
                self.final_results[key] = formatted_results
        except Exception as e:
            logging.error(f"Error processing final classification: {e}")
            raise

    def replace_indices_with_descriptions_in_key(self, key, character_info, parent_char_index=None):
        """
        Replace indices with descriptions in classification key.

        Parameters:
        key (dict): The classification key.
        character_info (dict): Dictionary containing character information.
        parent_char_index (str): The parent character index (used for recursion).

        Returns:
        dict: Updated classification key with descriptions.

        Exceptions:
        Exception: Any error that occurs during replacement.
        """
        try:
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
        except Exception as e:
            logging.error(f"Error replacing indices with descriptions: {e}")
            raise

    def convert_structure(self, node):
        """
        Convert classification structure.

        Parameters:
        node (dict): The classification node.

        Returns:
        dict: Converted classification structure.

        Exceptions:
        Exception: Any error that occurs during conversion.
        """
        try:
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
        except Exception as e:
            logging.error(f"Error converting structure: {e}")
            raise

    def combine_results(self, initial, secondary, state_key):
        """
        Combine initial and secondary classification results.

        Parameters:
        initial (dict): Initial classification result.
        secondary (dict): Secondary classification result.
        state_key (str): The state key.

        Returns:
        None

        Exceptions:
        ValueError: If there are conflicting types for the state key.
        Exception: Any other error that occurs during combination.
        """
        try:
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
        except Exception as e:
            logging.error(f"Error combining results: {e}")
            raise

    def generate_classification_key(self, data, current_step, parent_step=None):
        """
        Generate classification key.

        Parameters:
        data (dict): Classification data.
        current_step (int): The current step number.
        parent_step (int): The parent step number (used for recursion).

        Returns:
        None

        Exceptions:
        Exception: Any error that occurs during generation.
        """
        global step_counter
        try:
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
        except Exception as e:
            logging.error(f"Error generating classification key: {e}")
            raise

    def process_key(self, nexus_file_path, prompt_file_path, character_file_path):
        """
        Process the taxonomic key.

        Parameters:
        nexus_file_path (str): Path to the Nexus file.
        prompt_file_path (str): Path to the prompt messages file.
        character_file_path (str): Path to the character information file.

        Returns:
        None

        Exceptions:
        FileNotFoundError: If the file is not found.
        JSONDecodeError: If there is an error decoding the JSON file.
        Exception: Any other error that occurs during processing.
        """
        try:
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
            logging.info(classification_key)
            with open("classification_key.txt", "w", encoding='utf-8') as f:
                f.write(classification_key)
        except Exception as e:
            logging.error(f"Error processing taxonomic key: {e}")
            raise

    def generate_taxonomic_description(self, species_name, species_data, character_info, prompt_messages):
        """
        Generate taxonomic description.

        Parameters:
        species_name (str): Name of the species.
        species_data (dict): Data of the species.
        character_info (dict): Character information.
        prompt_messages (dict): Prompt messages.

        Returns:
        str: Generated taxonomic description.

        Exceptions:
        Exception: Any error that occurs during description generation.
        """
        try:
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
        except Exception as e:
            logging.error(f"Error generating taxonomic description: {e}")
            raise

    def process_description(self, matrix_file_path, character_info_file_path, output_file_path, prompt_file_path):
        """
        Process taxonomic descriptions.

        Parameters:
        matrix_file_path (str): Path to the matrix file.
        character_info_file_path (str): Path to the character information file.
        output_file_path (str): Path to the output file.
        prompt_file_path (str): Path to the prompt messages file.

        Returns:
        None

        Exceptions:
        FileNotFoundError: If the file is not found.
        JSONDecodeError: If there is an error decoding the JSON file.
        Exception: Any other error that occurs during processing.
        """
        try:
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

            logging.info(f"Taxonomic descriptions have been generated and saved to '{output_file_path}'.")
        except FileNotFoundError as e:
            logging.error(f"File not found: {e.filename}")
            raise
        except json.JSONDecodeError as e:
            logging.error(f"Error decoding JSON from file: {e}")
            raise
        except Exception as e:
            logging.error(f"Error processing descriptions: {e}")
            raise


# Example usage
config_file_path = "path/to/config.json"
taxon_gpt = TaxonGPT(config_file_path)

# Use paths from the configuration
taxon_gpt.process_key(taxon_gpt.paths["nexus_file_path"], taxon_gpt.paths["prompt_file_path"], taxon_gpt.paths["character_file_path"])
taxon_gpt.process_description(taxon_gpt.paths["matrix_file_path"], taxon_gpt.paths["character_file_path"], taxon_gpt.paths["output_file_path"], taxon_gpt.paths["prompt_file_path"])
