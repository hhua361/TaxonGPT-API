# part 0

# Import necessary packages
import json  # For handling JSON data
from openai import OpenAI  # For interacting with OpenAI API
import os  # For interacting with the operating system, such as file paths
import re  # For regular expressions, useful for pattern matching in strings
import pandas as pd  # For data manipulation and analysis


# Part 1

# Function to convert a letter to a number based on its position in the alphabet
def letter_to_number(letter):
    return str(ord(letter) - ord('A') + 10)


# Function to parse the matrix content from NEXUS format
def parse_matrix(matrix_content):
    data = []
    headers = []
    lines = matrix_content.strip().split('\n')
    for i in range(0, len(lines), 2):
        taxa = lines[i].strip().strip("'")  # Extract taxa name
        traits = lines[i + 1].strip()  # Extract traits for the taxa
        species_traits = []
        j = 0
        while j < len(traits):
            if traits[j] == '(':  # Handle compound states
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
                species_traits.append('Missing')  # Missing data
            elif traits[j] == '-':
                species_traits.append('Not Applicable')  # Not applicable data
            elif traits[j].isalpha():
                species_traits.append(letter_to_number(traits[j]))  # Convert letter to number
            else:
                species_traits.append(traits[j])  # Directly append the trait
            j += 1
        data.append([taxa] + species_traits)  # Append the parsed traits
    max_traits = max(len(row) - 1 for row in data)
    headers = ['taxa'] + [f'Character{i + 1}' for i in range(max_traits)]  # Create headers for DataFrame
    try:
        df = pd.DataFrame(data, columns=headers)  # Create DataFrame
        return df
    except Exception as e:
        print(f"Error creating DataFrame: {e}")
        return None


# Function to convert NEXUS file to CSV format
def convert_nexus_to_csv(file_path, output_path):
    try:
        encodings = ['utf-8', 'gbk', 'latin1']  # List of encodings to try
        for encoding in encodings:
            try:
                with open(file_path, 'r', encoding=encoding) as file:
                    content = file.read()
                print(f"Successfully read file with encoding: {encoding}")
                break
            except UnicodeDecodeError:
                print(f"Failed to read file with encoding: {encoding}")
                continue
        else:
            raise ValueError("Failed to read file with all attempted encodings.")

        # Extract the MATRIX section from the NEXUS file content
        matrix_content = re.search(r'MATRIX\s*(.*?)\s*;', content, re.DOTALL).group(1).strip()
        df = parse_matrix(matrix_content)  # Parse the matrix content into a DataFrame
        df.to_csv(output_path, index=False)  # Save DataFrame as CSV
        return df
    except FileNotFoundError:
        print(f"File {file_path} not found.")
    except Exception as e:
        print(f"Error: {e}")


# Function to build a knowledge graph from the parsed matrix
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
        knowledge_graph[taxa] = {'Characteristics': characteristics}
    return knowledge_graph


# Function to save the knowledge graph as a JSON file
def save_knowledge_graph_as_json(knowledge_graph, file_path):
    with open(file_path, 'w') as f:
        json.dump(knowledge_graph, f, indent=4)

# Function to convert NEXUS to knowledge graph and save as CSV and JSON
def nexus_to_knowledge_graph(nexus_file_path, csv_output_path, json_output_path):
    # Step 1: Convert NEXUS to CSV
    df = convert_nexus_to_csv(nexus_file_path, csv_output_path)

    if df is not None:
        # Step 2: Build the knowledge graph from the DataFrame
        knowledge_graph = build_knowledge_graph(df)

        # Step 3: Save the knowledge graph as a JSON file
        save_knowledge_graph_as_json(knowledge_graph, json_output_path)

        return knowledge_graph
    else:
        print("Failed to create the DataFrame from NEXUS file.")
        return None

# Function to parse CHARLABELS section of the NEXUS file
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

# Function to parse STATELABELS section of the NEXUS file
def parse_statelabels(statelabels_content):
    statelabels = {}
    lines = statelabels_content.strip().split("\n")
    current_char = None
    states = []

    for line in lines:
        if re.match(r'^\d+', line):
            if current_char is not None:
                statelabels[current_char] = states
            parts = line.split(' ', 1)
            current_char = int(parts[0])
            states = parts[1].strip().strip(',').split("' '")
            states = [state.strip("'") for state in states]
        else:
            additional_states = line.strip().strip(',').split("' '")
            additional_states = [state.strip("'") for state in additional_states]
            states.extend(additional_states)

    if current_char is not None:
        statelabels[current_char] = states

    return statelabels

# Function to combine CHARLABELS and STATELABELS into a single dictionary
def combine_labels_and_states(charlabels, statelabels):
    character_info = {}
    for char_index, description in charlabels.items():
        states = statelabels.get(char_index, [])
        state_dict = {str(i + 1): state for i, state in enumerate(states)}
        character_info[str(char_index)] = {
            "description": description,
            "states": state_dict
        }
    return character_info

# Function to extract sections from the NEXUS file content
def extract_nexus_sections(nexus_content):
    charlabels_content = ""
    statelabels_content = ""
    lines = nexus_content.strip().split("\n")
    in_charlabels = False
    in_statelabels = False

    for line in lines:
        if "CHARLABELS" in line:
            in_charlabels = True
            continue
        if "STATELABELS" in line:
            in_statelabels = True
            continue
        if ";" in line:
            in_charlabels = False
            in_statelabels = False

        if in_charlabels:
            charlabels_content += line + "\n"
        if in_statelabels:
            statelabels_content += line + "\n"

    return charlabels_content, statelabels_content

# Function to parse the NEXUS file and return character information
def parse_nexus_file(file_path):
    with open(file_path, 'r') as file:
        nexus_content = file.read()

    charlabels_content, statelabels_content = extract_nexus_sections(nexus_content)

    # Parse CHARLABELS section
    charlabels = parse_charlabels(charlabels_content)

    # Parse STATELABELS section
    statelabels = parse_statelabels(statelabels_content)

    # Combine parsed results into a character_info dictionary
    character_info = combine_labels_and_states(charlabels, statelabels)

    return character_info

def load_prompt_messages(file_path):
    with open(file_path, "r", encoding="utf-8") as file:
        return json.load(file)

def load_character_messages(file_path):
    with open(file_path, "r", encoding="utf-8") as file:
        return json.load(file)

# Example Usage
nexus_file_path = "D:/桌面/taxonomy_primary_result/The_GPT-4_result/Dataset_2 (The Equisetum species (horsetails)) 3/Information gain methods/nexdata"
csv_output_path = "D:/桌面/process_data_2.csv"
json_output_path = "D:/桌面/knowledge_graph.json"
prompt_file_path = "D:/桌面/taxonomy_primary_result/Taxonomic dataset materials/prompt_messages.json"
character_file_path = "D:/桌面/TEST-KG/nexus fix/updated_character_info.json"
# Step 1: Convert NEXUS to CSV and build knowledge graph
knowledge_graph = nexus_to_knowledge_graph(nexus_file_path, csv_output_path, json_output_path)

# Step 2: Parse Nexus file to get character info
character_info = load_character_messages(character_file_path)

# Step 3: upload the prompt information
prompt_messages = load_prompt_messages(prompt_file_path)

# Display the results
print("Knowledge Graph:")
print(json.dumps(knowledge_graph, indent=4, ensure_ascii=False))
print("\nCharacter Info:")
print(json.dumps(character_info, indent=4, ensure_ascii=False))


# Part 2
# Input the API key and morphological matrix

# Initialize the OpenAI client with the API key from environment variables
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# Set up the prompt for the API input using the client.chat.completions.create interface
# to conduct multi-turn conversations. Assign different roles in the conversation (user, assistant, system)
# to ensure all input information is fully conveyed to the API model.
# Replace the placeholder in the content template with actual data
content_with_data = prompt_messages["initial_character_messages"][3]["content_template"].format(
        knowledge_graph=json.dumps(knowledge_graph)
    )

# Create messages list
messages_initial = [
        prompt_messages["initial_character_messages"][0],
        prompt_messages["initial_character_messages"][1],
        prompt_messages["initial_character_messages"][2],
        {"role": "user", "content": content_with_data},
    ]

# Set various parameters to control the API response.
# Setting the temperature to 0 and limiting max_tokens to save costs and avoid long, redundant outputs.
initial_character_info = client.chat.completions.create(
    model="gpt-4o",
    messages=messages_initial,
    stop=None,
    max_tokens=1000,
    temperature=0,
    n=1
)

# Store the API call response results as a file.
# (For subsequent distributed API call loops, consider storing in environment variables for continuous calls and modifications).
initial_response = initial_character_info.choices[0].message.content

# If used as a whole pipeline to transfer the results, ignore this print.
# However, for debugging, you can use this print statement to check the response.
print(initial_response)


# Part 3

# Function to parse the classification result text into a dictionary format
def parse_classification_result(result_text):
    classification = {"Character": None, "States": {}}
    try:
        # Attempt to match the Character from the result text
        character_match = re.search(r'"Character": "([^"]+)"', result_text)
        if character_match:
            classification["Character"] = character_match.group(1)
        else:
            raise ValueError("Character not found in the result text.")

        # Attempt to match each State and the corresponding species
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
        # Decide whether to return an empty classification or raise an exception when an error occurs
        raise e  # Or return classification

    return classification

# Parse the initial classification response from the API
parsed_initial_classification = parse_classification_result(initial_response)
print(parsed_initial_classification)

# Function to generate groups from the classification result
def generate_groups_from_classification(classification_result):
    """
    Generate groups from classification result.

    :param classification_result: Dictionary containing the classification result
    :return: List of tuples, where each tuple contains a state and a list of species
    """
    groups = []
    for state, species_list in classification_result["States"].items():
        groups.append((state, species_list))
    return groups

# Generate groups from the parsed initial classification
groups = generate_groups_from_classification(parsed_initial_classification)
print(groups)


# Part 4

# API call function for continued grouping for each subgroup
def classify_group(group_species):
    # Create a sub-matrix for the group of species
    group_matrix = {species: knowledge_graph[species] for species in group_species}
    group_matrix_str = json.dumps(group_matrix, ensure_ascii=False)

    # Replace the placeholder in the content template with actual data
    content_with_data = prompt_messages["secondary_character_messages"][3]["content_template"].format(
        group_matrix_str=group_matrix_str
    )

    # Create messages list
    messages_secondary = [
        prompt_messages["secondary_character_messages"][0],
        prompt_messages["secondary_character_messages"][1],
        prompt_messages["secondary_character_messages"][2],
        {"role": "user", "content": content_with_data}
    ]

    # Make the API call to classify the group
    response = client.chat.completions.create(
        model="gpt-4o",
        messages=messages_secondary,
        stop=None,
        temperature=0,
        max_tokens=1000,
        n=1
    )
    result_secondary = response.choices[0].message.content

    # Replace the placeholder in the content template with actual data
    content_with_data = prompt_messages["JSON_format_messages"][3]["content_template"].format(
        result_secondary=result_secondary
    )

    # Create messages_JSON list
    messages_JSON1 = [
        prompt_messages["JSON_format_messages"][0],
        prompt_messages["JSON_format_messages"][1],
        prompt_messages["JSON_format_messages"][2],
        {"role": "user", "content": content_with_data}
    ]

    # Make the API call to format the response as JSON
    response = client.chat.completions.create(
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


# part 5

# Function to clean and extract JSON string
def extract_json_string(json_string):
    # Find the positions of the start and end of the JSON object
    start = json_string.find('{')
    end = json_string.rfind('}') + 1

    # If both start and end positions are valid, extract and return the JSON string
    if start != -1 and end != -1:
        cleaned_string = json_string[start:end]
        return cleaned_string.strip()

    # If positions are not valid, return an empty string
    return ""


def recursive_classification(groups, final_classification, classification_results, depth=0, max_depth=10):
    """
    Recursive classification function to process groups and store results.
    :param groups: Groups to be processed
    :param final_classification: Final classification result
    :param classification_results: Classification results
    :param depth: Current recursion depth
    :param max_depth: Maximum recursion depth
    :return: Final classification result
    """
    # Continue looping while the groups list is not empty
    # Initialize state and current_group for error handling
    state, current_group = None, []
    while groups:
        try:
            # Pop the first group from the list, getting the state and current group of species
            state, current_group = groups.pop(0)
            print(f"Processing group with state: {state}, species: {current_group}, at depth: {depth}")

            # If the current group has only one species, add it to the final classification
            if len(current_group) == 1:
                final_classification[current_group[0]] = current_group
            # If the current recursion depth has reached the maximum depth, stop further classification
            elif depth >= max_depth:
                print(f"Reached max depth {max_depth}. Stopping further classification for group: {current_group}")
                final_classification[state] = current_group
            else:
                # Call the classify_group function to classify the current group
                classification_result = classify_group(current_group)
                # Clean the API classification result to extract the JSON string
                cleaned_classification_result = extract_json_string(classification_result)
                # Store the classification result in classification_results
                classification_results[state] = cleaned_classification_result

                # Parse the classification result, create new subgroups, and add them to groups for further classification
                parsed_result = parse_classification_result(classification_result)
                new_groups = generate_groups_from_classification(parsed_result)

                # Recursively call itself to process new subgroups, increasing the recursion depth
                recursive_classification(new_groups, final_classification, classification_results, depth + 1, max_depth)

        except Exception as e:
            # Catch exceptions and print error messages
            print(f"Error processing group with state: {state}, species: {current_group}, at depth: {depth}")
            print(f"Exception: {e}")
            raise e

    return final_classification


# Part 6

# Assume the variables have been initialized
max_depth = 5  # Can be adjusted based on the hierarchical structure of input data and application requirements

# Dictionary to store the final classification where each species is classified individually
final_classification = {}

# Dictionary to store the API classification results for each state
classification_results = {}

# Print the initial state of groups and dictionaries for debugging purposes
print("Initial groups:", groups)
print("Initial final_classification:", final_classification)
print("Initial classification_results:", classification_results)

# Call the recursive_classification function to process the groups and store the results
final_classification = recursive_classification(groups, final_classification, classification_results, depth=0, max_depth=max_depth)

# Print the final classification results
print("Final Classification:")
print(json.dumps(final_classification, indent=2, ensure_ascii=False))

# Print the classification results from the API calls
print("\nClassification Results:")
print(classification_results)


# Part 7

# Reload the groups information to help with further processing
groups = generate_groups_from_classification(parsed_initial_classification)
print(classification_results)
print(type(classification_results))


# Function to extract paths from the classification tree
def extract_paths(node, path=None):
    if path is None:
        path = {}

    if 'Character' in node and 'States' in node:
        current_character = node['Character'].replace(" ", "").strip()
        for state, value in node['States'].items():
            new_path = path.copy()
            new_path[current_character] = state
            if isinstance(value, dict):
                yield from extract_paths(value, new_path)
            else:
                for species in value:
                    yield species, new_path

# Process each classification result and extract paths
final_results = {}

for key, json_str in classification_results.items():
    classification_data = json.loads(json_str)
    species_paths = list(extract_paths(classification_data))

    formatted_results = {}
    for species, path in species_paths:
        formatted_results[species] = {"Characteristics": path}

    final_results[key] = formatted_results


# Part 8

# Function to check if the state matches the correct state
def check_state_match(state, correct_state):
    if correct_state is None:
        return False
    if " and " in correct_state:
        correct_states = correct_state.split(" and ")
        return all(sub_state in correct_states for sub_state in state.split(" and "))
    return state == correct_state

# Validate classification results and log errors
def validate_results(final_results, knowledge_graph):
    errors = []
    for key, results in final_results.items():
        for species, data in results.items():
            if species in knowledge_graph:
                mismatch = False
                incorrect_character_states = {}
                for character, state in data["Characteristics"].items():
                    character = character.replace(" ", "").strip()
                    correct_state = knowledge_graph[species]["Characteristics"].get(character)
                    if correct_state is None or not check_state_match(state, correct_state):
                        mismatch = True
                        incorrect_character_states[character] = {"error_state": state, "correct_state": correct_state}
                if mismatch:
                    errors.append({
                        "species": species,
                        "key": key,
                        "error": "Mismatch",
                        "error_result": incorrect_character_states,
                        "correct_result": {character: knowledge_graph[species]["Characteristics"].get(character) for character in incorrect_character_states}
                    })
            else:
                errors.append({
                    "species": species,
                    "key": key,
                    "error": "Species not found in knowledge graph",
                    "error_result": data["Characteristics"]
                })
    return errors


# Part 9

# Function to get the species list for a specific state from the groups
def get_species_list_for_state(groups, key):
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


# Part 10

# Function to correct classification errors using the API
def correct_classification(errors, classification_results, knowledge_graph):
    for error in errors:
        key = error['key']

        # Get the species list for the erroneous state
        species_list = get_species_list_for_state(groups, key)
        if not species_list:
            continue

        # Create a sub-matrix for the group of species
        group_matrix = {s: knowledge_graph[s] for s in species_list}
        group_matrix_str = json.dumps(group_matrix, ensure_ascii=False)

        # Replace the placeholders in the content templates with actual data
        content_error = prompt_messages["correct_messages"][2]["content_template"].format(error=error)
        content_group_matrix = prompt_messages["correct_messages"][4]["content_template"].format(group_matrix_str=group_matrix_str)

        # Create messages list
        messages_correct = [
            prompt_messages["correct_messages"][0],
            prompt_messages["correct_messages"][1],
            {"role": "user", "content": content_error},
            prompt_messages["correct_messages"][3],
            {"role": "user", "content": content_group_matrix}
        ]

        # Make the API call to correct the classification
        response = client.chat.completions.create(
            model="gpt-4o",
            messages=messages_correct,
            stop=None,
            temperature=0,
            max_tokens=1000,
            n=1
        )
        corrected_result = response.choices[0].message.content

        # Replace the placeholder in the content template with actual data
        content_with_data = prompt_messages["JSON_format_messages"][3]["content_template"].format(
            result_secondary=corrected_result
        )

        # Create messages_JSON list
        messages_JSON2 = [
            prompt_messages["JSON_format_messages"][0],
            prompt_messages["JSON_format_messages"][1],
            prompt_messages["JSON_format_messages"][2],
            {"role": "user", "content": content_with_data}
        ]

        # Make the API call to format the response as JSON
        response = client.chat.completions.create(
            model="gpt-4o",
            messages=messages_JSON2,
            stop=None,
            temperature=0,
            max_tokens=1500,
            n=1
        )
        json_result = response.choices[0].message.content
        json_cleaned_result = extract_json_string(json_result)
        print(json_cleaned_result)
        classification_results[key] = json_cleaned_result
        return classification_results


# Part 11

# Validate the initial classification results and log any errors
errors = validate_results(final_results, knowledge_graph)

# Purpose: Enter a loop until all errors have been fixed.
# Function: Executes the code inside the loop when the errors list is not empty.
while errors:
    # Fix current categorization errors using the API
    classification_results = correct_classification(errors, classification_results, knowledge_graph)

    # Reset the final_results dictionary to store the corrected categorization results
    final_results = {}

    # Iterate over the corrected classification results and extract species classification paths
    for key, json_str in classification_results.items():
        classification_data = json.loads(json_str)
        species_paths = list(extract_paths(classification_data))

        # Format the extracted classification paths and store them in the formatted_results dictionary
        formatted_results = {}
        for species, path in species_paths:
            formatted_results[species] = {"Characteristics": path}

        # Add the formatted classification results to final_results
        final_results[key] = formatted_results

    # Re-validate the corrected classification results and log any remaining errors
    errors = validate_results(final_results, knowledge_graph)

# Save the final classification results to a JSON file
with open('final_classification.json', 'w') as f:
    json.dump(final_results, f, indent=4)
print("Final classification results have been saved to 'final_classification.json'.")
print(json.dumps(final_results, indent=4))


# Part 12

# Convert classification_results JSON strings to dictionaries
classification_result = {key: json.loads(value) for key, value in classification_results.items()}


# Recursive function to convert structure to the desired format
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


# Process classification results to the desired format
converted_result = {}
for key, value in classification_result.items():
    converted_result[f"Character {key}"] = convert_structure(value)


# Combine initial classification with other results
def combine_results(initial, secondary, state_key):
    if not secondary:
        return

    initial_states = initial["States"].get(state_key)
    if initial_states is None:
        initial["States"][state_key] = secondary
        return

    if isinstance(initial_states, list):
        if isinstance(secondary, list):
            initial["States"][state_key] = list(set(initial_states + secondary))  # Merge two lists and remove duplicates
        else:
            initial["States"][state_key] = secondary
    elif isinstance(initial_states, dict):
        if isinstance(secondary, dict):
            for key, value in secondary["States"].items():
                if key not in initial_states:
                    initial_states[key] = value
                else:
                    combine_results(initial_states, value, key)
        else:
            raise ValueError(f"Conflicting types for key {state_key}: {type(initial_states)} vs {type(secondary)}")
    else:
        raise ValueError(f"Unexpected type for initial states: {type(initial_states)}")


# Dynamically combine all secondary classification results
for state_key, secondary in classification_result.items():
    combine_results(parsed_initial_classification, secondary, state_key)

# Convert the merged results to the desired format
converted_initial_classification = convert_structure(parsed_initial_classification)

# Recursive function to replace indices with descriptions in the classification key
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
            state_key = f"State {' '.join(states)}: {';'.join(state_descriptions)}"
            if isinstance(subtree, dict):
                updated_key[state_key] = replace_indices_with_descriptions_in_key(subtree, character_info, parent_char_index)
            else:
                updated_key[state_key] = subtree
        else:
            updated_key[char_state] = subtree
    return updated_key


# Replace feature and state descriptions
updated_classification_key = replace_indices_with_descriptions_in_key(converted_initial_classification, character_info)
print(type(updated_classification_key))
# Print the updated classification key
print("Updated Classification Key:")
print(json.dumps(updated_classification_key, indent=4, ensure_ascii=False))



# Initialize step counter
step_counter = 1
steps = []

# Recursive function to generate classification key
def generate_classification_key(data, current_step, parent_step=None):
    global step_counter
    if isinstance(data, dict):
        state_steps = []
        step_map = {}
        for character, states in data.items():
            for state, next_level in states.items():
                full_state_description = f"{character.split(': ')[1]}：{state.split(': ')[1]}"  # Combine character and state descriptions
                if isinstance(next_level, dict):
                    step_counter += 1
                    next_step_prefix = str(step_counter)
                    state_steps.append(f"    - {full_state_description} ........ {next_step_prefix}")  # Use combined description
                    step_map[step_counter] = (next_level, current_step)
                else:
                    state_steps.append(f"    - {full_state_description} ........ {next_level}")  # Use combined description
        if parent_step:
            steps.append(f"{current_step}({parent_step}).")
        else:
            steps.append(f"{current_step}.")
        steps.extend(state_steps)
        for step, (next_level, parent_step) in step_map.items():
            generate_classification_key(next_level, step, parent_step)
    else:
        # If data is not a dictionary, do not recurse
        return

# Generate classification key
generate_classification_key(updated_classification_key, 1)

# Format output
classification_key = "\n".join(steps)
print(classification_key)

# Write results to file
with open("classification_key.txt", "w") as f:
    f.write(classification_key)




