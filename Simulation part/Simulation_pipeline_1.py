# The simulation pipeline 1: Test the ability to extract Nexus matrix information

import pprint
import json
from openai import OpenAI
import os
import random
import re
import pandas as pd

# Part 1: Randomly generate the character list information and store the result in a variable
number_about_the_character = 15
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
     "content": f"""Please randomly generate a character list and indicate the relevant species name, and strictly follow the above requirements.
     When generating the character list, please ensure that the list contains exactly {number_about_the_character} characters 
    """}
]

# Generate the initial character list using OpenAI API
response = client.chat.completions.create(
    model="gpt-4o-2024-08-06",
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
    # 找到 JSON 部分的起始位置
    json_start_index = character_list_str.find("```json")
    json_end_index = character_list_str.rfind("```")

    if json_start_index == -1 or json_end_index == -1:
        raise ValueError("Could not find JSON format in the character list string.")

    # 提取 JSON 字符串部分并移除包围的反引号
    json_str = character_list_str[json_start_index + len("```json"):json_end_index].strip()

    try:
        # 解析 JSON 字符串
        character_dict = json.loads(json_str)
    except json.JSONDecodeError as e:
        raise ValueError(f"JSON Decode Error: {e}")

    state_ranges = []

    # 遍历每个字符并提取其状态
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
            You are a taxonomic assistant.

            **Task:**
            - Generate accurate and complete taxonomic descriptions for each species by mapping character state information to species morphological matrices.

            **Specific Requirements:**

            1. **Description Language:** Write standard academic taxonomic descriptions in English.

            2. **Content Inclusion:** The descriptions need to include all characters from the morphological matrix and accurately correspond to each character's state.

            3. **Description Format:**
                - **List Form:** List each character's state description according to its number.
                - **Paragraph Form:** Describe all character states in a paragraph, indicating the character numbers at appropriate places.

            4. **Handling Multiple States:** For characters with multiple states (e.g., "1 and 2"), accurately reflect that the taxon possesses all these states. For example: "Character 5: possesses both wings and antennae."

            5. **Avoid Subjective Information:** Strictly generate descriptions based on the provided data without including any errors or assumed information. Avoid subjective judgments.

            6. **Terminology Consistency:** Use consistent professional terminology to ensure the descriptions are professional and consistent.

            7. **Separate Presentation:** The taxonomic descriptions for each taxon should be presented separately to avoid any loss of information or confusion due to space constraints.

            8. **Data Format:**
                - **Morphological Matrix (knowledge_graph):** Provided in JSON format, structured as follows:
                ```json
                {
                    "taxon1": {
                        "character1": "state1",
                        "character2": ["state1", "state2"],  // Multiple states
                        ...
                    },
                    ...
                }
                ```
                - **Character Information (character_list):** Provided in JSON format, structured as follows:
                ```json
                {
                    "character1": {
                        "description": "Description of character 1",
                        "states": {
                            "state1": "Description of state 1",
                            "state2": "Description of state 2",
                            ...
                        }
                    },
                    ...
                }
                ```

            9. **Example:**

            **List Form:**
            - **Character 1:** State description.
            - **Character 2:** State description.
            - ...

            **Paragraph Form:**
            "1. State description. 2. State description. ..."

            **Note:** Include character numbers in the paragraph form.
        """},
        {"role": "user", "content": f"""
            Please generate standard taxonomic descriptions for all taxa based on the provided morphological matrix and character information.

            **Morphological Matrix (knowledge_graph):**

            {knowledge_graph}

            **Character Information (character_list):**

            {character_list}

            **Note:**
            - For characters with multiple states, please accurately reflect that the taxon possesses all these states.
            - Please strictly generate descriptions based on the provided data, avoiding any additional details or explanations that are not provided.
            - Each taxon's description should be presented separately.

        """},
        {"role": "assistant", "content": """
            Understood. I will strictly generate standard academic taxonomic descriptions for each taxon according to the provided morphological matrix and character state information.

            I will provide each taxon's description in both list form and paragraph form, indicating character numbers in the paragraph form, and accurately reflecting multiple states.
        """}
    ]

    response = client.chat.completions.create(
            model="gpt-4o-2024-08-06",
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
        model="gpt-4o-2024-08-06",
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

