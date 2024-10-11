import json
from openai import OpenAI
import os
import re
import pandas as pd


class TaxonGPT:
    """
    A class to process taxonomic datasets and generate knowledge graphs using OpenAI's API.

    Attributes:
        config (dict): Configuration settings loaded from a JSON file.
        client (OpenAI): OpenAI client initialized with API key from the config.
        paths (dict): Paths for input and output files.
        knowledge_graph (dict): Knowledge graph generated from the dataset.
        character_info (dict): Information about character states.
        prompt_messages (dict): Prompt messages for OpenAI API calls.
        step_counter (int): Counter to keep track of steps in the process.
    """

    def __init__(self, config_file):
        """
        Initializes the TaxonGPT with configuration settings.

        Args:
            config_file (str): Path to the configuration file.
        """
        self.config = self.load_config(config_file)  # Load configuration from file
        self.client = OpenAI(api_key=self.config["api_key"])  # Initialize OpenAI client
        self.paths = self.config["paths"]  # Set paths for input and output files
        self.knowledge_graph = None  # Initialize knowledge graph as None
        self.character_info = None  # Initialize character info as None
        self.prompt_messages = None  # Initialize prompt messages as None
        self.step_counter = 1  # Initialize step counter

    def load_config(self, config_path):
        """
        Loads the configuration settings from a JSON file.

        Args:
            config_path (str): Path to the configuration file.

        Returns:
            dict: Configuration settings.
        """
        with open(config_path, 'r', encoding='utf-8') as config_file:
            config = json.load(config_file)  # Load JSON configuration
        return config

    def letter_to_number(self, letter):
        """
        Converts a letter to a number based on its position in the alphabet.

        Args:
            letter (str): The letter to convert.

        Returns:
            str: The corresponding number as a string.
        """
        return str(ord(letter) - ord('A') + 10)  # Convert letter to number

    def parse_matrix(self, matrix_content):
        """
        Parses the matrix content and converts it into a pandas DataFrame.

        Args:
            matrix_content (str): The content of the matrix to parse.

        Returns:
            pd.DataFrame: DataFrame containing the parsed matrix.
        """
        data = []
        headers = []
        lines = matrix_content.strip().split('\n')

        for i in range(0, len(lines), 2):
            taxa = lines[i].strip().strip("'")  # Get taxa name
            traits = lines[i + 1].strip()  # Get traits
            species_traits = []
            j = 0

            while j < len(traits):
                if traits[j] == '(':
                    j += 1
                    states = ''
                    while traits[j] != ')':
                        if traits[j].isalpha():
                            states += self.letter_to_number(traits[j])  # Convert letter to number
                        else:
                            states += traits[j]
                        j += 1
                    species_traits.append(','.join(states))
                elif traits[j] == '?':
                    species_traits.append('Missing')
                elif traits[j] == '-':
                    species_traits.append('Not Applicable')
                elif traits[j].isalpha():
                    species_traits.append(self.letter_to_number(traits[j]))  # Convert letter to number
                else:
                    species_traits.append(traits[j])
                j += 1

            data.append([taxa] + species_traits)  # Append parsed data

        max_traits = max(len(row) - 1 for row in data)
        headers = ['taxa'] + [f'Character{i + 1}' for i in range(max_traits)]

        try:
            df = pd.DataFrame(data, columns=headers)  # Create DataFrame
            return df
        except Exception as e:
            print(f"Error creating DataFrame: {e}")
            return None

    def convert_nexus_to_csv(self, file_path, output_path):
        """
        Converts a NEXUS file to a CSV file.

        Args:
            file_path (str): Path to the NEXUS file.
            output_path (str): Path to save the CSV file.

        Returns:
            pd.DataFrame: DataFrame containing the converted data.
        """
        try:
            encodings = ['utf-8', 'gbk', 'latin1']

            for encoding in encodings:
                try:
                    with open(file_path, 'r', encoding=encoding) as file:
                        content = file.read()  # Read file content
                    print(f"Successfully read file with encoding: {encoding}")
                    break
                except UnicodeDecodeError:
                    print(f"Failed to read file with encoding: {encoding}")
                    continue
            else:
                raise ValueError("Failed to read file with all attempted encodings.")

            matrix_content = re.search(r'MATRIX\s*(.*?)\s*;', content, re.DOTALL).group(1).strip()
            df = self.parse_matrix(matrix_content)  # Parse matrix content
            df.to_csv(output_path, index=False)  # Save DataFrame to CSV
            return df
        except FileNotFoundError:
            print(f"File {file_path} not found.")
        except Exception as e:
            print(f"Error: {e}")

    def build_knowledge_graph(self, matrix):
        """
        Builds a knowledge graph from the given matrix.

        Args:
            matrix (pd.DataFrame): DataFrame containing the matrix data.

        Returns:
            dict: Knowledge graph.
        """
        knowledge_graph = {}

        for _, row in matrix.iterrows():
            taxa = row.iloc[0]  # Get taxa name
            characteristics = {}

            for col in matrix.columns[1:]:
                state = row[col]

                if isinstance(state, str) and ',' in state:
                    state = state.replace(',', ' and ')

                characteristics[col] = str(state)  # Assign state to characteristic

            knowledge_graph[taxa] = {'Characteristics': characteristics}  # Append to knowledge graph

        return knowledge_graph

    def save_knowledge_graph_as_json(self, knowledge_graph, file_path):
        """
        Saves the knowledge graph as a JSON file.

        Args:
            knowledge_graph (dict): The knowledge graph to save.
            file_path (str): Path to save the JSON file.
        """
        with open(file_path, 'w') as f:
            json.dump(knowledge_graph, f, indent=4)  # Save knowledge graph to JSON

    def nexus_to_knowledge_graph(self):
        """
        Converts a NEXUS file to a knowledge graph and saves it as a JSON file.

        Returns:
            dict: The generated knowledge graph.
        """
        nexus_file_path = self.paths["nexus_file_path"]
        csv_output_path = self.paths["csv_output_path"]
        json_output_path = self.paths["json_output_path"]

        df = self.convert_nexus_to_csv(nexus_file_path, csv_output_path)  # Convert NEXUS to CSV

        if df is not None:
            self.knowledge_graph = self.build_knowledge_graph(df)  # Build knowledge graph
            self.save_knowledge_graph_as_json(self.knowledge_graph, json_output_path)  # Save knowledge graph to JSON
            return self.knowledge_graph
        else:
            print("Failed to create the DataFrame from NEXUS file.")
            return None

    def load_prompt_messages(self):
        """
        Loads prompt messages from a file.

        Returns:
            dict: Loaded prompt messages.
        """
        prompt_file_path = self.paths["prompt_file_path"]

        with open(prompt_file_path, "r", encoding="utf-8") as file:
            self.prompt_messages = json.load(file)  # Load prompt messages from JSON

        return self.prompt_messages

    def load_character_messages(self):
        """
        Loads character messages from a file.

        Returns:
            dict: Loaded character messages.
        """
        character_file_path = self.paths["character_file_path"]

        with open(character_file_path, "r", encoding="utf-8") as file:
            self.character_info = json.load(file)  # Load character messages from JSON

        return self.character_info

    def initial_api_call(self):
        """
        Makes an initial API call to OpenAI with the loaded prompt messages.

        Returns:
            str: Initial response from the API.
        """
        content_with_data = self.prompt_messages["initial_character_messages"][3]["content_template"].format(
            knowledge_graph=json.dumps(self.knowledge_graph)  # Insert knowledge graph into template
        )

        messages_initial = [
            self.prompt_messages["initial_character_messages"][0],
            self.prompt_messages["initial_character_messages"][1],
            self.prompt_messages["initial_character_messages"][2],
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

        initial_response = initial_character_info.choices[0].message.content
        return initial_response

    def parse_classification_result(self, result_text):
        """
        Parses the classification result from the API, which contains a JSON block embedded in textual data.

        Args:
            result_text (str): The result text from the API, which includes extra text around a JSON block.

        Returns:
            dict: Parsed classification result containing 'Character' and 'States'.
        """
        classification = {"Character": None, "States": {}}

        try:
            # Use regular expression to extract the JSON content
            json_match = re.search(r'\{.*\}', result_text, re.DOTALL)

            if not json_match:
                raise ValueError("No valid JSON content found in the result text.")

            # Extract the JSON portion
            json_content = json_match.group(0)

            # Parse the JSON content into a dictionary
            result_json = json.loads(json_content)

            # Check for the 'Character' field
            if "Character" in result_json:
                classification["Character"] = result_json["Character"]
            else:
                raise ValueError("Character field not found in the result text.")

            # Check for the 'States' field
            if "States" in result_json and isinstance(result_json["States"], dict):
                classification["States"] = result_json["States"]
            else:
                raise ValueError("No valid 'States' found in the result text.")

        except json.JSONDecodeError as e:
            print(f"Error decoding the result text as JSON: {e}")
            raise ValueError("Invalid JSON format.")
        except Exception as e:
            print(f"Error parsing classification result: {e}")
            raise e

        return classification

    def compare_and_correct_species(self, api_output):
        """
        Compares and corrects species classification based on the knowledge graph.

        Args:
            api_output (dict): API output classification result.

        Returns:
            dict: Corrected classification result.
        """
        input_species = list(self.knowledge_graph.keys())
        api_species = []

        for state, species_list in api_output["States"].items():
            api_species.extend(species_list)

        missing_species = [species for species in input_species if species not in api_species]
        print("Missing species: ", missing_species)
        character = api_output["Character"]

        for species in missing_species:
            state = self.knowledge_graph[species]["Characteristics"].get(character, None)

            if state:
                if state in api_output["States"]:
                    api_output["States"][state].append(species)
                else:
                    api_output["States"][state] = [species]

        return api_output

    def generate_groups_from_classification(self, classification_result):
        """
        Generates groups from the classification result.

        Args:
            classification_result (dict): Classification result.

        Returns:
            list: Groups generated from the classification.
        """
        groups = []

        for state, species_list in classification_result["States"].items():
            groups.append((state, species_list))

        return groups

    def classify_group(self, group_species):
        """
        Classifies a group of species using the API.

        Args:
            group_species (list): List of species to classify.

        Returns:
            str: JSON formatted classification result from the API.
        """
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

    def extract_json_string(self, json_string):
        """
        Extracts a JSON string from the given string, ensuring no invalid characters.

        Args:
            json_string (str): String containing JSON data.

        Returns:
            str: Extracted and cleaned JSON string.
        """
        start = json_string.find('{')
        end = json_string.rfind('}') + 1

        if start != -1 and end != -1:
            cleaned_string = json_string[start:end].strip()

            # Remove invalid characters, such as the prefix 'n'
            if cleaned_string.startswith('n'):
                cleaned_string = cleaned_string[1:].strip()

            return cleaned_string

        return ""

    def recursive_classification(self, groups, final_classification, classification_results, depth=0, max_depth=10):
        """
        Recursively classifies groups, creating a hierarchical structure.

        Args:
            groups (list): List of species groups.
            final_classification (dict): The final classification result being built.
            classification_results (dict): Stores intermediate classification results.
            depth (int): The current recursion depth.
            max_depth (int): The maximum allowed depth for classification.

        Returns:
            dict: The final classification result.
        """
        state, current_group = None, []
        while groups:
            try:
                state, current_group = groups.pop(0)
                print(f"Processing group with state: {state}, species: {current_group}, at depth: {depth}")

                if isinstance(current_group, list) and len(current_group) == 1:
                    final_classification[current_group[0]] = current_group
                elif depth >= max_depth:
                    print(f"Reached max depth {max_depth}. Stopping further classification for group: {current_group}")
                    final_classification[state] = current_group
                elif isinstance(current_group, dict):
                    next_character = current_group.get("Character")
                    next_states = current_group.get("States", {})
                    print(f"Found nested group, next Character: {next_character}, States: {next_states}")
                    new_groups = [(s, species) for s, species in next_states.items()]
                    self.recursive_classification(new_groups, final_classification, classification_results, depth + 1,
                                                  max_depth)
                else:
                    classification_result = self.classify_group(current_group)
                    cleaned_classification_result = self.extract_json_string(classification_result)
                    # Check if the extracted JSON is valid
                    if not cleaned_classification_result or cleaned_classification_result == "":
                        raise ValueError(f"Extracted JSON string is invalid: {classification_result}")

                    print(f"Extracted JSON: {cleaned_classification_result}")

                    classification_results[state] = cleaned_classification_result
                    parsed_result = self.parse_classification_result(classification_result)
                    new_groups = self.generate_groups_from_classification(parsed_result)
                    self.recursive_classification(new_groups, final_classification, classification_results, depth + 1,
                                                  max_depth)
            except Exception as e:
                print(f"Error processing group with state: {state}, species: {current_group}, at depth: {depth}")
                print(f"Exception: {e}")
                raise e
        return final_classification

    def extract_paths(self, node, path=None):
        """
        Extracts paths from the classification node.

        Args:
            node (dict): Classification node.
            path (dict): Current path.

        Yields:
            tuple: Species and their corresponding paths.
        """
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

    def check_state_match(self, state, correct_state):
        """
        Checks if the state matches the correct state.

        Args:
            state (str): The state to check.
            correct_state (str): The correct state to compare against.

        Returns:
            bool: True if the states match, False otherwise.
        """
        if correct_state is None:
            return False

        if " and " in correct_state:
            correct_states = correct_state.split(" and ")
            return all(sub_state in correct_states for sub_state in state.split(" and "))

        return state == correct_state

    def validate_results(self, final_results, groups):
        """
        Validates the final classification results.

        Args:
            final_results (dict): Final classification results.
            groups (list): List of species groups.

        Returns:
            list: List of errors found in the results.
        """
        errors = []
        all_species = set(self.knowledge_graph.keys())
        classified_species = set()

        for key, results in final_results.items():
            for species, data in results.items():
                classified_species.add(species)

                if species in self.knowledge_graph:
                    mismatch = False
                    incorrect_character_states = {}

                    for character, state in data["Characteristics"].items():
                        character = character.replace(" ", "").strip()
                        correct_state = self.knowledge_graph[species]["Characteristics"].get(character)

                        if correct_state is None or not self.check_state_match(state, correct_state):
                            mismatch = True
                            incorrect_character_states[character] = {"error_state": state,
                                                                     "correct_state": correct_state}

                    if mismatch:
                        errors.append({
                            "species": species,
                            "key": key,
                            "error": "Mismatch",
                            "error_result": incorrect_character_states,
                            "correct_result": {
                                character: self.knowledge_graph[species]["Characteristics"].get(character) for character
                                in incorrect_character_states}
                        })
                else:
                    errors.append({
                        "species": species,
                        "key": key,
                        "error": "Species not found in knowledge graph",
                        "error_result": data["Characteristics"]
                    })

        missing_species = all_species - classified_species

        for species in missing_species:
            group_found = False

            for group_key, species_list in groups:
                if species in species_list:
                    errors.append({
                        "species": species,
                        "error": "Missing species",
                        "key": group_key,
                        "correct_result": self.knowledge_graph[species]["Characteristics"]
                    })
                    group_found = True
                    break

            if not group_found:
                errors.append({
                    "species": species,
                    "error": "Missing species",
                    "key": None,
                    "correct_result": self.knowledge_graph[species]["Characteristics"]
                })

        return errors

    def get_species_list_for_state(self, groups, key):
        """
        Gets the list of species for a given state.

        Args:
            groups (list): List of species groups.
            key (str): State key.

        Returns:
            list: List of species for the state.
        """
        species_list = []

        for state, species in groups:
            if state == key:
                species_list = species
                break

        if not species_list:
            print(f"Key {key} not found in groups")
        else:
            print(f"Processing species list for state '{key}': {species_list}")

        return species_list

    def correct_classification(self, errors, classification_results, groups):
        """
        Corrects the classification based on errors.

        Args:
            errors (list): List of errors to correct.
            classification_results (dict): Current classification results.
            groups (list): List of species groups.

        Returns:
            dict: Updated classification results.
        """
        for error in errors:
            key = error['key']

            if key is None:
                continue

            species_list = self.get_species_list_for_state(groups, key)

            if not species_list:
                continue

            group_matrix = {s: self.knowledge_graph[s] for s in species_list}
            group_matrix_str = json.dumps(group_matrix, ensure_ascii=False)
            content_error = self.prompt_messages["correct_messages"][2]["content_template"].format(error=error)
            content_group_matrix = self.prompt_messages["correct_messages"][4]["content_template"].format(
                group_matrix_str=group_matrix_str)

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
            classification_results[key] = json_cleaned_result
            return classification_results

    def convert_structure(self, node):
        """
        Converts the structure of the classification node.

        Args:
            node (dict): Classification node.

        Returns:
            dict: Converted structure.
        """
        if "Character" in node and "States" in node:
            character = node["Character"]
            states = node["States"]
            converted = {f"Character {character.replace('Character', '')}": {}}

            for state, sub_node in states.items():
                state_key = f"State {state}"

                if isinstance(sub_node, list):
                    converted[f"Character {character.replace('Character', '')}"][state_key] = sub_node[0] if len(
                        sub_node) == 1 else sub_node
                elif isinstance(sub_node, dict):
                    converted[f"Character {character.replace('Character', '')}"][state_key] = self.convert_structure(
                        sub_node)

            return converted

        return node

    def combine_results(self, initial, secondary, state_key):
        """
        Combines initial and secondary results.

        Args:
            initial (dict): Initial classification result.
            secondary (dict): Secondary classification result.
            state_key (str): State key to combine results for.
        """
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

    def replace_indices_with_descriptions_in_key(self, key, parent_char_index=None):
        """
        Replaces indices with descriptions in the classification key.

        Args:
            key (dict): Classification key.
            parent_char_index (str): Parent character index.

        Returns:
            dict: Updated classification key with descriptions.
        """
        updated_key = {}

        for char_state, subtree in key.items():
            if char_state.startswith("Character"):
                parts = char_state.split()

                if len(parts) > 1:
                    char_index = parts[1]

                    if char_index in self.character_info:
                        char_description = f"Character {char_index}: {self.character_info[char_index]['description']}"

                        if isinstance(subtree, dict):
                            updated_subtree = self.replace_indices_with_descriptions_in_key(subtree, char_index)
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
                    descriptions = [self.character_info[parent_char_index]["states"].get(s.strip(), "") for s in
                                    individual_states]
                    state_descriptions.append(" and ".join(filter(None, descriptions)))

                state_key = f"State {' '.join(states)}: {';'.join(state_descriptions)}"

                if isinstance(subtree, dict):
                    updated_key[state_key] = self.replace_indices_with_descriptions_in_key(subtree, parent_char_index)
                else:
                    updated_key[state_key] = subtree
            else:
                updated_key[char_state] = subtree

        return updated_key

    def generate_classification_key(self, data, current_step, parent_step=None):
        """
        Generates a classification key from the data.

        Args:
            data (dict): Classification data.
            current_step (int): Current step in the classification process.
            parent_step (int): Parent step in the classification process.
        """
        global step_counter

        if isinstance(data, dict):
            state_steps = []
            step_map = {}

            for character, states in data.items():
                for state, next_level in states.items():
                    # Split character and state and check if split result has enough parts
                    character_parts = character.split(':')
                    state_parts = state.split(': ')

                    if len(character_parts) > 1 and len(state_parts) > 1:
                        full_state_description = f"{character_parts[1]}: {state_parts[1]}"
                    else:
                        # Provide a default or handle cases where the expected split is not present
                        full_state_description = f"{character}: {state}"
                        print(
                            f"Warning: character or state not in expected format. Character: {character}, State: {state}")

                    # Check if next_level is a dictionary and handle accordingly
                    if isinstance(next_level, dict):
                        self.step_counter += 1
                        next_step_prefix = str(self.step_counter)
                        state_steps.append(f"    - {full_state_description} ........ {next_step_prefix}")
                        step_map[self.step_counter] = (next_level, current_step)
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

    def process_key(self):
        """
        Processes the key by converting NEXUS to a knowledge graph, loading messages,
        making initial API calls, parsing classification results, recursively classifying groups,
        and finally generating the classification key.
        """
        # Convert NEXUS to knowledge graph and load messages
        self.nexus_to_knowledge_graph()  # Convert NEXUS file to a knowledge graph
        self.load_character_messages()  # Load messages related to species characteristics
        self.load_prompt_messages()  # Load messages related to prompts
        initial_response_result = self.initial_api_call()  # Make an initial API call and retrieve results
        print(initial_response_result)  # Output the initial result returned by the API

        # Parse API output, correct species names, and generate classification groups
        parsed_api_output = self.parse_classification_result(initial_response_result)  # Parse classification result
        print(type(parsed_api_output))  # Output the type of parsed result
        corrected_api_output = self.compare_and_correct_species(parsed_api_output)  # Compare and correct species
        groups = self.generate_groups_from_classification(
            corrected_api_output)  # Generate groups based on classification result
        print(groups)  # Output the generated groups

        # Recursively classify the groups with a set maximum depth
        max_depth = 5  # Set the maximum depth for recursive classification
        final_classification = {}
        classification_results = {}
        final_classification = self.recursive_classification(groups, final_classification, classification_results,
                                                             depth=0, max_depth=max_depth)
        groups = self.generate_groups_from_classification(corrected_api_output)  # Regenerate groups

        # Extract paths and format the classification results
        final_results = {}
        for key, json_str in classification_results.items():
            classification_data = json.loads(json_str)  # Parse JSON string into Python object
            species_paths = list(self.extract_paths(classification_data))  # Extract species classification paths

            formatted_results = {}
            for species, path in species_paths:
                formatted_results[species] = {
                    "Characteristics": path}  # Store the paths as characteristics for each species

            final_results[key] = formatted_results  # Save the formatted results in the final results

        # Validate the classification results and correct any errors
        errors = self.validate_results(final_results, groups)  # Validate if there are errors in the final results
        print(errors)  # Output the found errors
        correction_attempts = 0  # Initialize a counter for the number of correction attempts
        max_correction_attempts = 10  # Set the maximum number of correction attempts

        while errors and correction_attempts < max_correction_attempts:
            correction_attempts += 1  # Increment the correction attempt counter
            classification_results = self.correct_classification(errors, classification_results,
                                                                 groups)  # Attempt to correct classification errors
            final_results = {}  # Reinitialize the final results

            for key, json_str in classification_results.items():
                try:
                    classification_data = json.loads(json_str)  # Attempt to parse the JSON data
                except json.JSONDecodeError as e:
                    print(f"Error decoding JSON for key {key}: {e}")  # Output the JSON decoding error
                    print(f"Invalid JSON string: {json_str}")  # Output the invalid JSON data
                    raise

                species_paths = list(self.extract_paths(classification_data))  # Extract species paths
                formatted_results = {}

                for species, path in species_paths:
                    formatted_results[species] = {"Characteristics": path}  # Format species paths as characteristics

                final_results[key] = formatted_results  # Save the formatted results

            errors = self.validate_results(final_results, groups)  # Validate classification results again

        if correction_attempts == 0:
            print("No errors found. The initial classification results are correct.")  # Output if no errors were found
        else:
            print(
                f"Errors were corrected {correction_attempts} times before finalizing the results.")  # Output how many times errors were corrected

        if correction_attempts >= max_correction_attempts:
            print(
                "Due to the API repeatedly correcting errors, an infinite loop has been triggered. It is recommended to restart the code execution process to avoid endlessly correcting the same issue."
            )  # Output warning if max correction attempts are reached

        # Save the final classification results as a JSON file
        with open('final_classification.json', 'w') as f:
            json.dump(final_results, f, indent=4)
        print("Final classification results have been saved to 'final_classification.json'.")
        print(json.dumps(final_results, indent=4))  # Output the final results

        classification_result = {key: json.loads(value) for key, value in
                                 classification_results.items()}  # Convert results to a dictionary

        # Convert data structure, combine results, and generate the classification key
        converted_result = {}
        for key, value in classification_result.items():
            converted_result[f"Character {key}"] = self.convert_structure(value)  # Convert structure

        for state_key, secondary in classification_result.items():
            self.combine_results(corrected_api_output, secondary, state_key)  # Combine classification results

        # Update the classification key
        converted_initial_classification = self.convert_structure(corrected_api_output)
        updated_classification_key = self.replace_indices_with_descriptions_in_key(converted_initial_classification,
                                                                                   self.character_info)
        print(type(updated_classification_key))  # Output the type of updated classification key
        print("Updated Classification Key:")
        print(json.dumps(updated_classification_key, indent=4,
                         ensure_ascii=False))  # Output the updated classification key

        # Generate classification steps
        self.step_counter = 1  # Initialize step counter
        self.steps = []  # Initialize steps list
        self.generate_classification_key(updated_classification_key, 1)  # Generate classification key

        classification_key = "\n".join(self.steps)  # Join steps into a single string
        print(classification_key)  # Output the classification key

        # Get the output file path for the classification key from the configuration
        taxonomic_key_path = self.config["paths"]["taxonomic_key_path"]

        # Write the classification key to a file
        with open(taxonomic_key_path, "w") as f:
            f.write(classification_key)
        print(f"Taxonomic key has been saved to '{taxonomic_key_path}'.")  # Output the save path

    def generate_taxonomic_description(self, species_name, species_data):
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
            content_with_data = self.prompt_messages["description_messages"][4]["content_template"].format(
                species_name=species_name,
                species_data=json.dumps(species_data),
                character_info=json.dumps(self.character_info)
            )

            messages = [
                self.prompt_messages["description_messages"][0],
                self.prompt_messages["description_messages"][1],
                self.prompt_messages["description_messages"][2],
                self.prompt_messages["description_messages"][3],
                {"role": "user", "content": content_with_data},
                self.prompt_messages["description_messages"][5]
            ]

            response = self.client.chat.completions.create(
                model="gpt-4o-2024-08-06",
                messages=messages,
                stop=None,
                temperature=0,
                n=1
            )

            result = response.choices[0].message.content
            print(result)
            return result

        except Exception as e:
            print(f"Error generating taxonomic description: {e}")
            raise

    def load_json_file(self, file_path):
        """
        Loads a JSON file from the specified file path.

        Args:
            file_path (str): The path to the JSON file to be loaded.

        Returns:
            dict: The parsed JSON data as a Python dictionary.
        """
        with open(file_path, 'r', encoding='utf-8') as file:
            return json.load(file)

    def parse_list_form(self, description_text):
        """
        Parse the List Format or List Form description and return a dictionary mapping character numbers to state numbers.

        Args:
            description_text (str): The text containing the taxonomic description.

        Returns:
            dict: A dictionary mapping character numbers to state numbers.
        """
        # Ensure description_text is a string
        if not isinstance(description_text, str):
            print("Error: description_text is not a string.")
            return {}

        character_states = {}

        # Extract the "List Form" or "List Format" section
        list_form_match = re.search(r'#### List (Form|Format):\n(.*?)(\n####|\Z)', description_text, re.DOTALL)

        if not list_form_match:
            print("Unable to find the 'List Form' or 'List Format' section.")
            return character_states

        list_form_text = list_form_match.group(2).strip()
        # Split the content by lines
        lines = list_form_text.split('\n')
        idx = 0
        while idx < len(lines):
            line = lines[idx].strip()
            # Check if the line starts with a number and period, e.g., "1."
            match = re.match(r'^(\d+)\.\s*(.*)', line)
            if match:
                char_num = match.group(1)
                rest_of_line = match.group(2)
                idx += 1
                # Merge multi-line descriptions
                while idx < len(lines) and not re.match(r'^\d+\.\s', lines[idx].strip()):
                    rest_of_line += ' ' + lines[idx].strip()
                    idx += 1
                # Find all numbers in parentheses
                state_numbers = re.findall(r'\((\d+)\)', rest_of_line)
                if not state_numbers:
                    # Check for "Missing" or "Not Applicable" status.
                    if 'Missing' in rest_of_line:
                        state_numbers = ['Missing']
                    elif 'Not Applicable' in rest_of_line:
                        state_numbers = ['Not Applicable']
                character_states['Character' + char_num] = state_numbers
            else:
                idx += 1
        return character_states

    def parse_original_data(self, species_name):
        """
        Parses the original data from the knowledge graph and returns a dictionary mapping character numbers to state numbers.

        Args:
            species_name (str): The name of the species whose data needs to be parsed.

        Returns:
            dict: A dictionary mapping character numbers to lists of state numbers.
        """
        # Using data from knowledge_graph
        if species_name not in self.knowledge_graph:
            print(f"Error: {species_name} not found in the knowledge graph.")
            return {}

        characteristics = self.knowledge_graph[species_name]["Characteristics"]
        character_states = {}

        for char, states_str in characteristics.items():
            if states_str == "Missing":
                states_list = ['Missing']
            else:
                # Split the state string into a list, supporting "and" and comma separation.
                states_list = [s.strip() for s in re.split(r'and|,', states_str)]
            character_states[char] = states_list

        return character_states

    def compare_character_states(self, extracted_states, original_states):
        """
        Compares the extracted states with the original states and returns a list of mismatches.

        Args:
            extracted_states (dict): The character states extracted from the description.
            original_states (dict): The original character states from the knowledge graph.

        Returns:
            list: A list of mismatches, each represented as a dictionary.
        """
        mismatches = []
        for char in original_states:
            orig_states = original_states[char]
            extracted_states_char = extracted_states.get(char, [])
            if set(orig_states) != set(extracted_states_char):
                mismatches.append({
                    'Character': char,
                    'OriginalStates': orig_states,
                    'ExtractedStates': extracted_states_char
                })
        return mismatches

    def check_description(self, description_text, original_data, species_name):
        """
        Compares the character states in the provided description text with the original data for a given species.

        Args:
            description_text (str): The taxonomic description of the species in text format.
            original_data (dict): The original data containing species and their characteristics.
            species_name (str): The name of the species whose data needs to be compared.

        Returns:
            None: Prints the mismatches found, if any, or confirms that all character states match.
        """
        extracted_states = self.parse_list_form(description_text)
        original_states = self.parse_original_data(species_name)
        mismatches = self.compare_character_states(extracted_states, original_states)
        if mismatches:
            print(f"Mismatches found for {species_name}:")
            for m in mismatches:
                print(
                    f"{m['Character']}: Original states {m['OriginalStates']}, Extracted states {m['ExtractedStates']}")
        else:
            print(f"All character states match for {species_name}.")

    def compare_files(self, description_file_path, knowledge_graph_file_path):
        """
        Loads and compares the description and original data from files, performing a check for each species.

        Args:
            description_file_path (str): The file path to the JSON file containing the taxonomic descriptions.
            knowledge_graph_file_path (str): The file path to the JSON file containing the original knowledge graph data.

        Returns:
            None: Iterates over each species in the description file and runs the check for mismatches.
        """
        # Load file data
        description_data = self.load_json_file(description_file_path)
        print(description_data)
        knowledge_graph_data = self.load_json_file(knowledge_graph_file_path)

        # Initialize a variable to store the comparison results
        comparison_results = []

        # Iterate over each species in the description file
        for species_name in description_data:
            print(f"\nChecking data for {species_name}...")
            description_text = description_data[species_name]
            original_data = knowledge_graph_data

            # Run the description check function
            mismatches = self.check_description(description_text, original_data, species_name)

            if mismatches:
                comparison_results.append({
                    "species": species_name,
                    "mismatches": mismatches
                })

            # Save comparison results to a file
        comparison_output_path = self.config["paths"].get("comparison_output_path", "comparison_results.json")

        try:
            with open(comparison_output_path, 'w') as f:
                json.dump(comparison_results, f, indent=4)
            print(f"Comparison results have been saved to '{comparison_output_path}'.")
        except Exception as e:
            print(f"Error saving comparison results: {e}")

    def process_description(self):
        """
        Process taxonomic descriptions.

        Parameters:
        None

        Returns:
        None

        Exceptions:
        FileNotFoundError: If the file is not found.
        JSONDecodeError: If there is an error decoding the JSON file.
        Exception: Any other error that occurs during processing.
        """
        self.nexus_to_knowledge_graph()
        self.load_character_messages()
        self.load_prompt_messages()

        taxonomic_descriptions = {}

        # Loop through species and generate descriptions
        for species_name, species_data in self.knowledge_graph.items():
            try:
                description = self.generate_taxonomic_description(species_name, species_data)
                taxonomic_descriptions[species_name] = description
            except Exception as e:
                print(f"Error generating description for species {species_name}: {e}")
                continue

        try:
            # Get the output file path from the configuration
            output_file_path = self.config["paths"]["taxonomic_description_path"]

            # Save the taxonomic descriptions to the specified file
            with open(output_file_path, 'w') as f:
                json.dump(taxonomic_descriptions, f, indent=4)
            print(f"Taxonomic descriptions have been saved to '{taxonomic_description_path}'.")
        except Exception as e:
            print(f"Error saving taxonomic descriptions to file: {e}")

        # Optional: Check function control, not implemented by default
        if self.config.get("enable_description_check", True):
            description_file_path = self.config["paths"]["taxonomic_description_path"]
            knowledge_graph_file_path = self.config["paths"]["json_output_path"]
            self.compare_files(description_file_path, knowledge_graph_file_path)  # Call the check function
        else:
            print("Description check is disabled by configuration.")


# The config.json file template
"""
{
    "api_key": "YOUR API KEY HERE",
    "nexus_file_path": "<Full path to the input Nexus file>",
    "prompt_file_path": "<Full path to the input Prompt file>",
    "character_file_path": "<Full path to the input character info file>",

    "csv_output_path": "<Full path to  output CSV format matrix file>",
    "json_output_path": "<Full path to output JSON format matrix file>",
    "taxonomic_description_path": "<Full path to output taxonomic description file>"
    "taxonomic_key_path": "<Full path to output taxonomic key file>"


    "comparison_output_path": "<Full path to output taxonomic key file>",
    # By default, the description check feature is disabled to prevent generating excessive redundant results. If you need to check the execution steps, please set "enable_description_check": false to true in the configuration file.
    "enable_description_check": false

}
"""

# Get the path to the directory where the current script is located
script_directory = os.getcwd()

# Path to build configuration file (current directory)
config_file_path = os.path.join(script_directory, 'config.json')

# Check if the configuration file exists
if not os.path.exists(config_file_path):
    raise FileNotFoundError(f"Configuration file not found: {config_file_path}")

# Open and read the contents of the configuration file
with open(config_file_path, 'r') as config_file:
    config_data = json.load(config_file)

# Print the read configuration data
print(f"Read the profile data: {config_data}")

# Through TaxonGPT() to generate the related result
TaxonGPT = TaxonGPT(config_file_path)
# Generate the Taxonomic Key
TaxonGPT.process_key()
# Generate the Taxonomic Description
TaxonGPT.process_description()
