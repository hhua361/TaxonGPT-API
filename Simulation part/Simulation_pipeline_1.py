# The simulation pipeline 1: Test the ability to extract Nexus matrix information

import pprint
import json
from openai import OpenAI
import os
import random
import re
import pandas as pd

# Part 1: Randomly generate the character list information and store the result in a variable

# Initialize the OpenAI client with the API key
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# Messages to guide the generation of the character list
messages_character_list = [
    {"role": "system",
     "content":
         """You are now an expert in taxonomic research.
         Utilizing your knowledge in taxonomy, your task is to randomly generate a character list for a specific group of organisms.
         The character list should include the following:
         1. Character Descriptions: Provide detailed descriptions for each character.
         2. State Descriptions: Generate descriptions for the various states associated with each character.
         3. Taxonomic Principles: Ensure that the relationships between characters and their states are consistent with taxonomic principles, and the character and state description need to follow taxonomic principles.
         Please ensure that the character list is specific to a single taxonomic group. The final output should be presented in the following format:
         """},
    {"role": "system",
     "content": """Please make the result follow these formats:
            Species name:
            Character list format:
            {
            "1": {
                "description": "Detailed description of Character1",
                "states": {
                    "1": "Character1, State1",
                    "2": "Character1, State2"
                }
            },
            "2": {
                "description": "Detailed description of Character2",
                "states": {
                    "1": "Character2, State1",
                    "2": "Character2, State2",
                    "3": "Character2, State3"
                }
            },
            ...
            }
     """},
    {"role": "user",
     "content": """Please randomly generate a character list and indicate the relevant species name, and strictly follow the above requirements.
                Generate as many characters as you can."""}
]

# Generate the initial character list using OpenAI API
response = client.chat.completions.create(
    model="gpt-4o",
    messages=messages_character_list,
    stop=None,
    max_tokens=1000,
    temperature=0,
    n=1
)
character_list = response.choices[0].message.content
print(character_list)


# Part 2: Parse and process the character list into a dictionary format

def parse_character_list(character_list_str):
    """
    Parse the character list string into a dictionary format.

    Args:
        character_list_str (str): The character list in string format.

    Returns:
        list: A list of state ranges for each character.
    """
    json_start_index = character_list_str.find("Character list format:")
    if json_start_index == -1:
        raise ValueError("Could not find 'Character list format:' in the character list string.")

    json_str = character_list_str[json_start_index + len("Character list format:"):].strip()

    json_start_index = json_str.find("{")

    if json_start_index == -1:
        raise ValueError("Could not find JSON start '{' after 'Character list format:'.")

    json_str = json_str[json_start_index:]

    try:
        character_dict = json.loads(json_str)
    except json.JSONDecodeError as e:
        raise ValueError(f"JSON Decode Error: {e}")

    state_ranges = []
    for character in character_dict.values():
        states = list(character['states'].keys())
        state_ranges.append([int(state) for state in states])

    return state_ranges

def generate_random_matrix(num_species, state_ranges):
    """
    Generate a random matrix of character states for a given number of species.

    Args:
        num_species (int): The number of species to generate.
        state_ranges (list): A list of state ranges for each character.

    Returns:
        list: A matrix of randomly generated character states for each species.
    """
    matrix = []

    for i in range(num_species):
        species_name = f"SPECIES {i + 1}"
        states = []

        for states_for_character in state_ranges:
            rand_choice = random.random()
            if rand_choice < 0.1:  # 10% chance of missing state
                state = '-'
            elif rand_choice < 0.3:  # 20% chance of multiple states
                state_combination = random.sample(states_for_character, k=random.randint(2, len(states_for_character)))
                state_combination.sort()
                state = f"({''.join(map(str, state_combination))})"
            else:  # 70% chance of a single state
                state = str(random.choice(states_for_character))

            states.append(state)

        matrix.append([species_name] + states)

    return matrix

def print_matrix(matrix):
    """
    Print the matrix in a readable format.

    Args:
        matrix (list): The matrix to be printed.
    """
    for row in matrix:
        print("\t".join(row))

# Parse the character list into state ranges
state_ranges = parse_character_list(character_list)
print(state_ranges)

# Define the number of species to generate
num_species = 5
# Generate the random matrix
matrix = generate_random_matrix(num_species, state_ranges)
print(matrix)
print_matrix(matrix)

# Part 3: Generate the description based on the character list and matrix information

def convert_matrix_to_knowledge_graph(matrix):
    """
    Convert a species matrix into a knowledge graph format.

    Args:
        matrix (list): A matrix containing species name and character states.

    Returns:
        dict: A dictionary representing the knowledge graph of the species.
    """
    species_name = matrix[0]
    characteristics = {}

    for i, state in enumerate(matrix[1:], start=1):
        if state == '-':
            characteristics[f"Character{i}"] = "Missing"
        elif state.startswith('(') and state.endswith(')'):
            states = state[1:-1]
            state_desc = " or ".join([f"state {s}" for s in states])
            characteristics[f"Character{i}"] = state_desc
        else:
            characteristics[f"Character{i}"] = f"state {state}"

    return {species_name: {"Characteristics": characteristics}}

def call_api_for_description(knowledge_graph, character_list):
    """
    Generate taxonomic descriptions using OpenAI API based on the knowledge graph and character list.

    Args:
        knowledge_graph (dict): The knowledge graph of a species.
        character_list (str): The character list in string format.

    Returns:
        str: The generated taxonomic description.
    """
    messages = [
        {"role": "system", "content": """
            1. You are a Taxonomic Assistant.
            2. You specialize in generating accurate and complete taxonomic descriptions by mapping feature state information to species morphology matrices.
            3. Utilize your natural language skills to generate accurate taxonomic descriptions for each species!
            Specific requirements:
            **Generate standard academic taxonomic descriptions, which need to include all characters in the morphological matrix and accurately correspond to the state of each character. 
            **Generate descriptions in list form and paragraph form. In paragraph form, the number of each character should be indicated.
            """},
        {"role": "user", "content": """
            1. Generate taxonomic descriptions from the morphological matrix without including any false information.
            2. Based on the provided morphological matrix (presented as a knowledge graph in JSON format), generate standard taxonomic descriptions for all taxa in the matrix.
            3. Additional character labels and state labels will be provided, containing detailed descriptions of each character and its corresponding state.
            4. Multiple states in the matrix (e.g., '1 and 2') indicate that the character of that TAXA has both state 1 and state 2.
            """},
        {"role": "assistant", "content": """
            Sure, I know how to generate a taxonomic description, and I will handle the multiple states in the description.
            I will follow these specific requirements:
            1. Generate standard academic taxonomic descriptions strictly corresponding to the morphological matrix and eigenstate information.
            2. For the generated taxonomy descriptions, I will generate separate descriptions in list form and paragraph form.
            """},
            {"role": "user", "content":f"""
            Due to the large number of results, to avoid space constraints, please show the taxonomic description of each taxon separately.
            Here is the morphological matrix for species{knowledge_graph}.
                f"Here is the character info: {character_list}.
             """},
            {"role": "assistant", "content":
                "I will step by step show the results."
             }
        ]
    response = client.chat.completions.create(
            model="gpt-4o",
            messages=messages,
            stop=None,
            temperature=0,
            n=1
        )
    description_content = response.choices[0].message.content
    return description_content

# Global variable to store species descriptions
species_descriptions_dict = {}

def process_species(matrix, character_list):
    """
    Process each species matrix to generate taxonomic descriptions.

    Args:
        matrix (list): A matrix containing species names and character states.
        character_list (str): The character list in string format.

    Returns:
        dict: A dictionary with species names as keys and their corresponding descriptions as values.
    """
    global species_descriptions_dict
    species_descriptions = {}

    for species_matrix in matrix:
        knowledge_graph = convert_matrix_to_knowledge_graph(species_matrix)
        description = call_api_for_description(knowledge_graph,character_list)
        species_name = species_matrix[0]
        species_descriptions[species_name] = description

    species_descriptions_dict.update(species_descriptions)
    return species_descriptions

# Generate species descriptions
species_descriptions = process_species(matrix,character_list)

# Print each species description
for species_name, description in species_descriptions_dict.items():
    print(f"Description for {species_name}:\n{description}\n")

def extract_matrix_from_description(species_name, description, character_list):
    """
    Extract the matrix information from a taxonomic description using OpenAI API.

    Args:
        species_name (str): The name of the species.
        description (str): The taxonomic description of the species.
        character_list (str): The character list in string format.

    Returns:
        str: The extracted matrix information.
    """
    messages_extract_information = [
        {"role": "system",
         "content": """
             You are an expert in taxonomic information extraction, skilled in extracting morphological character information from standard taxonomic descriptions based on a given character list.
             The character list specifies different characters and their states for all species in the dataset.
             Please generate a list-form extraction result for each species, listing the state of each trait.
             """},
        {"role": "system",
         "content": """
            To extract character information, follow these steps:
            First, check if the species description includes any mention of the character's states. If it does, correctly record the corresponding state label.
            If the description does not mention any character states, use your language reasoning skills to strictly check for words indicating the absence of the characteristic (e.g., "non," "no," "not"). If such terms are present, use the corresponding state label based on your reasoning.
            If there is no mention of the character's states in the species description and your reasoning confirms the absence of relevant content, use "Gap" to represent this.

            In the given character list, each character and state has a corresponding number.
            Please indicate the number for each trait's state in the generated list for each species.
            If a trait state does not exist, which will called "Missing" it symbol as '-'.
            """},
        {"role": "system",
         "content": """
            After generating the extraction results in list format, please sort the traits and their corresponding states for each species in ascending order, from left to right.
            In the example, the first '1' indicates that character 1 has state number 1 for the species.
            Arrange the list format results accurately as shown in the example.
            For content with multiple feature states use (12) to indicate that the CHARACTER has both states of serial number 1, 2.
            """},
        {"role": "system",
         "content": """
             Please make the result follow these formats,and don't need to show any other things, please only show the below results:
             Matrix information:
             SPECIES NAME : 1 2 1 3 3 (12) 2 (13)
             """},
        {"role": "user",
         "content": f"""
         Here is the character list {character_list} 
         Here is the corresponding taxonomic description for{species_name}:{description}"
         """},

    ]
    response = client.chat.completions.create(
        model="gpt-4o",
        messages=messages_extract_information,
        stop=None,
        max_tokens=1000,
        temperature=0,
        n=1
    )
    matrix_information = response.choices[0].message.content
    return matrix_information

# Extract matrices from descriptions and store in a dictionary
matrix_results = {}
for species_name, description in species_descriptions_dict.items():
    matrix_info = extract_matrix_from_description(species_name, description, character_list)
    matrix_results[species_name] = matrix_info

# Print or process the extracted matrix information
for species_name, matrix_info in matrix_results.items():
    print(f"Matrix for {species_name}:\n{matrix_info}\n")
print(matrix_results['SPECIES 1'])

def clean_extracted_matrix(matrix_str):
    """
    Clean the extracted matrix string to remove irrelevant information and retain the actual matrix content.

    Args:
        matrix_str (str): The extracted matrix string.

    Returns:
        str: The cleaned matrix string.
    """
    cleaned_matrix = re.sub(r"^.*?:\s*\*.*?\*\s*:\s*", "", matrix_str)
    return cleaned_matrix.strip()


def compare_matrices(initial_matrix, extracted_matrix_results):
    """
    Compare the initial matrix with the extracted matrix to identify differences.

    Args:
        initial_matrix (list): The initial randomly generated matrix.
        extracted_matrix_results (dict): The matrix extracted from descriptions.

    Returns:
        list: A list of comparison results for each species.
    """
    comparison_results = []

    # Iterate through each species in the initial matrix
    for species_data in initial_matrix:
        species_name = species_data[0]
        initial_matrix_values = species_data[1:]

        # Retrieve the extracted matrix for comparison
        if species_name in extracted_matrix_results:
            extracted_matrix_str = extracted_matrix_results[species_name]
            extracted_matrix_cleaned = clean_extracted_matrix(extracted_matrix_str)
            extracted_matrix_values = extracted_matrix_cleaned.split()

            differences = []

            # Compare the initial and extracted matrices
            for i, (initial_value, extracted_value) in enumerate(zip(initial_matrix_values, extracted_matrix_values)):
                if initial_value != extracted_value:
                    differences.append(f"Character {i + 1}: Initial='{initial_value}' vs Extracted='{extracted_value}'")  # 记录差异

            if differences:
                comparison_results.append({
                    "species": species_name,
                    "initial_matrix": " ".join(initial_matrix_values),
                    "extracted_matrix": extracted_matrix_cleaned,
                    "differences": differences
                })
            else:
                comparison_results.append({
                    "species": species_name,
                    "initial_matrix": " ".join(initial_matrix_values),
                    "extracted_matrix": extracted_matrix_cleaned,
                    "differences": "NO"
                })
        else:
            comparison_results.append({
                "species": species_name,
                "initial_matrix": " ".join(initial_matrix_values),
                "extracted_matrix": "Not Found",
                "differences": "Species not found in extracted matrix results."
            })

    return comparison_results

# Compare the initial and extracted matrices
comparison_results = compare_matrices(matrix, matrix_results)

# Print the comparison results
for result in comparison_results:
    print(f"Initial Matrix：{result['species']}: {result['initial_matrix']}")
    print(f"Extract Matrix：{result['species']}: {result['extracted_matrix']}")
    if isinstance(result['differences'], list):
        print("Differences: " + ", ".join(result['differences']))
    else:
        print(f"Differences: {result['differences']}")
    print()  # Blank line after each species

