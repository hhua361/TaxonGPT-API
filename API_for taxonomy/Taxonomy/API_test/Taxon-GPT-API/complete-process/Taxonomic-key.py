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

# Example Usage
nexus_file_path = "D:/桌面/taxonomy_primary_result/The_GPT-4_result/Dataset_3 (The Lycopodiales (Diphasiastrum, Huperzia, Isoetes, Lycopodium, Selaginella)) 4/Information gain methods/nexdata"
csv_output_path = "D:/桌面/process_data_2.csv"
json_output_path = "D:/桌面/knowledge_graph.json"

# Step 1: Convert NEXUS to CSV and build knowledge graph
knowledge_graph = nexus_to_knowledge_graph(nexus_file_path, csv_output_path, json_output_path)

# Step 2: Parse Nexus file to get character info
character_info = parse_nexus_file(nexus_file_path)

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
messages_initial = [
    # Set the system role to focus on taxonomy tasks.
    # Emphasize the system's understanding of morphological matrices, information gain,
    # and the construction of classification keys in the system setup.
    {"role": "system",
     "content":
         """You are a helpful taxonomist assistant.
         You are skilled at calculating the correct information gain to choose the character that best divides species into even groups based on their states.
         Based on the selected character, classify the species into different groups according to their states.
         For each group with more than two species, continue selecting characters to further classify this group until each group only has one species.
         After multiple classifications, determine the final classification levels and record each classifying character and its state. 
         Finally, generate a taxonomic key.
         You need to strictly ensure that you categorize all species when selecting the initial character, and that you don't ignore any of the species.
         Please format the classification result as follows:
        ```
        {
            "Character": "Character1",
            "States": {
                "State 1": ["species1", "species2", ...],
                "State 2": ["species3", "species4", ...],
                "State ...": ["species5", "species6", ...]
            }
        }
        ```
        Ensure that the response follows this format exactly.
        Additionally, exactly ensure that all species are included in the initial classification result.
         """},

    # Input the main task request, construct the classification key, and emphasize the details needed for classification.
    # This includes: the main objective, information gain calculation, ignoring invalid states, clarifying multi-character states,
    # guiding correct selection based on the significance of information gain, and standardizing the final output format for subsequent extraction of API results.
    {"role": "system",
     "content": """
                Generate the taxonomic key based on the provided morphological matrix. The matrix includes all species and their different states for each character.
                The process involves selecting a character to classify the species into groups. Repeat this classification within each subgroup until each group contains only one species.
                Information gain measures how much the uncertainty in the dataset is reduced after using a character for classification. It helps in selecting characters that minimize the entropy of the subset after classification, leading to better classification results.
                Please select the initial classification character for all species based on the morphological matrix and information gain methods.
                In the morphological matrix, 'Missing' and 'Not applicable' are invalid states. If a character has invalid states for the group being classified, it should be ignored.
                States are represented by numbers, and '1 and 2' means multiple states should be treated as a single state type. For example, '3' and '2 and 3' are different states; these are two separate states, so when choosing a character, distinguish the species based on different states.
                You need to calculate the information gain for each character and choose the highest information gain result. The higher the Information Gain result, the greater the contribution of the feature to the classification.
                Now I will show you the morphological matrix. Please provide only the initial classification character and the categorization of species based on its state, and you should label this as # initial character classify result #
            """},

    # Use the assistant to summarize and refine the prompt content for the API.
    # Through the conversation with the assistant, deepen the API understanding of the content to some extent,
    # control the API response results, and standardize the output format of the API response.
    {"role": "assistant",
     "content": """
                Understood. I will generate the taxonomic key based on the provided morphological matrix. Here is a summary of the steps I will follow:
                1. The matrix includes all species and their different states for each character.
                2. I will select a character to classify the species into groups and repeat this classification within each subgroup until each group contains only one species, and I'll not ignore any species.
                3. I will use information gain to measure how much the uncertainty in the dataset is reduced after using a feature for classification. This helps in selecting features that minimize the entropy of the subset after classification, leading to better classification results.
                4. I will select the initial classification character for all species based on the morphological matrix and information gain methods.
                5. In the morphological matrix, 'Missing' and 'Not applicable' are considered invalid states. If a character has invalid states for the group being classified, it will be ignored.
                6. States are represented by numbers. For example, '1 and 2' means multiple states should be treated as a single state type. For example, '1' and '1 and 2' are different states; these are two separate states, so when choosing a character, distinguish the species based on different states.
                7. I will use information gain to calculate all characters and choose the highest information gain result. The higher the Information Gain result, the greater the contribution of the feature to the classification. I need to ensure the result is average classification.
                8. The final result will provide only the initial classification character and the categorization of species based on its state.
                9. I will use all the species in their entirety, strictly making sure to categorize all of them! (need to make sure to contain all species)
                10. Don't need to show how I calculate, only need to show the final result, and please show the final result in #initial character classify result# block, ensuring no errors where the state and species don't match.
                Please provide the morphological matrix data so that I can proceed with the initial classification.
            """},

    # Input the corresponding morphological matrix information for analysis.
    {"role": "user",
     "content": f"Here is morphological matrix:{knowledge_graph}"}
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

    # Define the messages for the API call
    messages_secondary = [
        # System role to focus on taxonomy tasks and ensure correct classification
        {"role": "system",
         "content":
             """
             You are a helpful taxonomist assistant.
             You are skilled at calculating the correct information gain to choose the character that best divides species into even groups based on their states.
             Based on the selected character, classify the species into different groups according to their states.
             For each group with more than two species, continue selecting characters to further classify this group until each group only has one species.
             After multiple classifications, determine the final classification levels and record each classifying character and its state.
             Finally, generate a taxonomic key.
             ***IMPORTANT: Ensure that each group contains only one species in the final classification result. Don't appear the result like state: [species A, species B], need to choose character to continue classifying these two species***
             """},
        {"role": "system",
         "content":
             """
             Generate the nested taxonomic key based on the provided morphological matrix.
             The process involves selecting a character to classify the species into groups. Repeat this classification within each subgroup until each group contains only one species.
             Information gain measures how much the uncertainty in the dataset is reduced after using a character for classification. It helps in selecting characters that minimize the entropy of the subset after classification, leading to better classification results.
             Please select the classification character for these group's species based on the morphological matrix and information gain methods.
             In the morphological matrix, 'Missing' and 'Not applicable' are invalid states. If a character has invalid states for the group being classified, it should be ignored.
             States are represented by numbers. For example, '1 and 2' means multiple states should be treated as a single state type and this multi-state characterization should not be confused with the single states within it (the state of '3' and '2 and 3' is different state, when you choose the character to based on the state to distinguish need to careful handle). The initial character should have no more than three state types.
             You need to calculate the information gain for each character and choose the highest information gain result. The higher the information gain result, the greater the contribution of the feature to the classification.
             After selecting the initial classification character and categorizing the species based on its state, repeat the process within each subgroup. For each subgroup, select the character with the highest information gain to further classify the species. Continue this process recursively until each group contains only one species.
             Now I will show you the morphological matrix. Please provide the classification character and the categorization of species based on its state. Then, continue to classify each subgroup recursively, showing the chosen character and categorization for each subgroup. Please present the result in a structured format, with each step clearly labeled.
             Please don't show how you analyze and calculate, please show me the final result.
             """},
        {"role": "assistant",
         "content":
             """
             Understood. I will generate the nested taxonomic key based on the provided morphological matrix. Here is a summary of the steps I will follow:
             1. The matrix includes all species and their different states for each character.
             2. I will select a character to classify the species into groups and repeat this classification within each subgroup until each group contains only one species.
             3. I will use information gain to measure how much the uncertainty in the dataset is reduced after using a feature for classification. This helps in selecting features that minimize the entropy of the subset after classification, leading to better classification results.
             4. I will select the classification character for the group's species based on the morphological matrix and information gain methods.
             5. In the morphological matrix, 'Missing' and 'Not applicable' are considered invalid states. If a character has invalid states for the group being classified, it will be ignored.
             6. States are represented by numbers. For example, '2 and 3' means multiple states should be treated as a single state type, and this multi-state characterization should not be confused with the individual states (like '2', '3') within it (such as '3' and '2 and 3' are different states, these are two separate states, when I choose a character based on different states to distinguish the species). The classification character should have no more than three state types.
             7. I will use information gain to calculate all characters and choose the highest information gain result. The higher the information gain result, the greater the contribution of the feature to the classification.
             8. The final result will provide only the initial classification character and the categorization of species based on its state.
             9. Don't need to show how the process about choosing, only need to show the final result as a nested structure, and I will store the result in #character classify result# block.
             Please provide the group morphological matrix data so that I can proceed with the classification.
             """},
        {"role": "user", "content": f"Here is the group information need to be classified and includes the morphological matrix {group_matrix_str}"}
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

    # Define messages for formatting the response to JSON
    messages_JSON = [
        {"role": "system",
         "content":
             """
             You are a helpful JSON format converter.
             You can express the nested structure as a JSON result based on the corresponding content.
             """},
        {"role": "system",
         "content":
             """
             Please format the classification result as follows:
             ```
             # Final taxonomic key result JSON format #
             {
                 "Character": "CharacterX",
                 "States": {
                     "1": ["speciesA"],
                     "2": {
                         "Character": "CharacterY",
                         "States": {
                             "1": ["speciesB"],
                             "2": ["speciesC"]
                         }
                     }
                 }
             }
             ```
             Ensure that the response follows this format exactly.
             """},
        {"role": "assistant",
         "content":
             """
             Understood. I'll convert the nested structure you gave me into JSON format and store it in #final result#.
             Please provide what you need to convert the format.
             """},
        {"role": "user", "content": f"Here are the taxonomic results for the nested schema representation {result_secondary}"}
    ]

    # Make the API call to format the response as JSON
    response = client.chat.completions.create(
        model="gpt-4o",
        messages=messages_JSON,
        stop=None,
        temperature=0,
        max_tokens=1500,
        n=1
    )
    json_result = response.choices[0].message.content
    print(json_result)
    return json_result


# part 4
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


# part 5
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

        # Define the messages for the API call to correct classification
        messages2 = [
            {"role": "system",
             "content": """
             You are a helpful taxonomist assistant.
             You are skilled at calculating the correct information gain to choose the character that best divides species into even groups based on their states.
             Based on the selected character, classify the species into different groups according to their states.
             For each group with more than two species, continue selecting characters to further classify this group until each group only has one species.
             After multiple classifications, determine the final classification levels and record each classifying character and its state.
             Finally, generate a taxonomic key.
             You are able to avoid the same error in your results based on the corrected results previously passed to you
             ***IMPORTANT: Ensure that each group contains only one species in the final classification result. Don't appear the result like state: [species A, species B]***
             """},
            {"role": "system",
             "content": """
             Generate the nested taxonomic key based on the provided morphological matrix.
             The process involves selecting a character to classify the species into groups. Repeat this classification within each subgroup until each group contains only one species.
             Information gain measures how much the uncertainty in the dataset is reduced after using a character for classification. It helps in selecting characters that minimize the entropy of the subset after classification, leading to better classification results.
             Please select the classification character for these group's species based on the morphological matrix and information gain methods.
             In the morphological matrix, 'Missing' and 'Not applicable' are invalid states. If a character has invalid states for the group being classified, it should be ignored.
             States are represented by numbers. For example, '1 and 2' means multiple states should be treated as a single state type and this multi-state characterization should not be confused with the single states within it (the state of '3' and '2 and 3' are different states, when you choose the character to based on the state to distinguish need to careful handle). The initial character should have no more than three state types.
             You need to calculate the information gain for each character and choose the highest information gain result. The higher the information gain result, the greater the contribution of the feature to the classification.
             After selecting the initial classification character and categorizing the species based on its state, repeat the process within each subgroup. For each subgroup, select the character with the highest information gain to further classify the species. Continue this process recursively until each group contains only one species.
             In the results, each group should contain only one species; need to choose suitable character.
             Now I will show you the morphological matrix. Please provide the classification character and the categorization of species based on its state. Then, continue to classify each subgroup recursively, showing the chosen character and categorization for each subgroup. Please present the result in a structured format, with each step clearly labeled.
             Please don't show how you analyze and calculate, please show me the final result.
             """},
            {"role": "user", "content": f"""
            This is the result of the error you generated in the previous API call. 
            In this file I have provided you with the CORRECT result. 
            Please strictly adhere to the use of the correct species feature status message! {error}
            """},
            {"role": "assistant", "content": f"""
            I will strictly use the correct species feature state information for evaluation, 
            while I will avoid using these incorrect feature state information that appeared previously in the classification results.
            """},
            {"role": "user", "content": f"Here is the group information need to be classified and includes the morphological matrix {group_matrix_str}"}
        ]

        # Make the API call to correct the classification
        response = client.chat.completions.create(
            model="gpt-4o",
            messages=messages2,
            stop=None,
            temperature=0,
            max_tokens=1000,
            n=1
        )
        corrected_result = response.choices[0].message.content

        # Define messages for formatting the corrected response as JSON
        messages_JSON = [
            {"role": "system",
             "content":
                 """
                 You are a helpful JSON format converter.
                 You can express the nested structure as a JSON result based on the corresponding content.
                 """},
            {"role": "system",
             "content":
                 """
                 Please format the classification result as follows:
                 ```
                 # Final taxonomic key result JSON format #
                 {
                     "Character": "CharacterX",
                     "States": {
                         "1": ["speciesA"],
                         "2": {
                             "Character": "CharacterY",
                             "States": {
                                 "1": ["speciesB"],
                                 "2": ["speciesC"]
                             }
                         }
                     }
                 }
                 ```
                 Ensure that the response follows this format exactly.
                 """},
            {"role": "assistant",
             "content":
                 """
                 Understood. I'll convert the nested structure you gave me into JSON format and store it in #final result#.
                 Please provide what you need to convert the format.
                 """},
            {"role": "user", "content": f"Here are the taxonomic results for the nested schema representation {corrected_result}"}
        ]

        # Make the API call to format the corrected response as JSON
        response = client.chat.completions.create(
            model="gpt-4o",
            messages=messages_JSON,
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
            state_key = f"State {' '.join(states)}: {' / '.join(state_descriptions)}"
            if isinstance(subtree, dict):
                updated_key[state_key] = replace_indices_with_descriptions_in_key(subtree, character_info, parent_char_index)
            else:
                updated_key[state_key] = subtree
        else:
            updated_key[char_state] = subtree
    return updated_key


# Replace feature and state descriptions
updated_classification_key = replace_indices_with_descriptions_in_key(converted_initial_classification, character_info)

# Print the updated classification key
print("Updated Classification Key:")
print(json.dumps(updated_classification_key, indent=4, ensure_ascii=False))


# Part 13

# Example initial result
initial_result = parsed_initial_classification

# Parse the API response JSON strings into dictionaries
parsed_classification_results = {key: json.loads(value) for key, value in classification_results.items()}

# Function to combine the initial and secondary classification results
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


# Dynamically combine all secondary classification results into the initial result
for state_key, secondary in parsed_classification_results.items():
    combine_results(initial_result, secondary, state_key)


# Function to display the final classification result in a readable format
def display_classification(result, indent=0):
    indent_space = " " * indent
    character = result.get("Character")
    states = result.get("States")

    classification = {}
    if character and states:
        classification["Character"] = character
        classification["States"] = {}
        print(f"{indent_space}1. **{character}:**")
        for state, species in states.items():
            if isinstance(species, list):
                print(f"{indent_space}   - State \"{state}\": {', '.join(species)}")
                classification["States"][state] = species
            elif isinstance(species, dict):
                print(f"{indent_space}   - State \"{state}\":")
                classification["States"][state] = display_classification(species, indent + 4)
    return classification

# Display the final classification result
final_result = display_classification(initial_result)
# Uncomment the lines below to print the final result as JSON
# print("\nFinal Result JSON:")
# print(json.dumps(final_result, indent=2))
