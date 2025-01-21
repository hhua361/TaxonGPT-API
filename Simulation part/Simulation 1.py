import json
from openai import OpenAI
import os
import random
import re
from typing import Dict, Set, Optional

# Initialize the OpenAI client using the API key from the environment variable
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# Define the number of characters and species to generate in the character list and Matrix
number_about_the_character = 10
num_species = 5

# Define messages to guide the generation of the character list
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

# Generate the initial character list using the OpenAI API
response = client.chat.completions.create(
    model="gpt-4o-2024-08-06",
    messages=messages_character_list,
    stop=None,
    max_tokens=1000,
    temperature=0,
    n=1
)

# Extract the generated character list
character_list_1 = response.choices[0].message.content

# Print the generated character list
print(character_list_1)

# Function to parse and process the character list into a dictionary format
def parse_character_list(character_list_str):
    """
    Parse the character list string into a list of state ranges for each character.

    Args:
        character_list_str (str): The character list in string format.

    Returns:
        list: A list of state ranges for each character, where each state range
              is a list of integers representing available states.

    Raises:
        ValueError: If the JSON format is not found or parsing fails.
    """
    # Locate the JSON section in the input string
    json_start_index = character_list_str.find("```json")
    json_end_index = character_list_str.rfind("```")

    if json_start_index == -1 or json_end_index == -1:
        raise ValueError("Could not find JSON format in the character list string.")

    # Extract and clean the JSON part
    json_str = character_list_str[json_start_index + len("```json"):json_end_index].strip()

    try:
        # Parse the JSON string into a dictionary
        character_dict = json.loads(json_str)
    except json.JSONDecodeError as e:
        raise ValueError(f"JSON Decode Error: {e}")

    # Extract state ranges from the parsed character dictionary
    state_ranges = []
    for character in character_dict.values():
        states = list(character['states'].keys())
        state_ranges.append([int(state) for state in states])

    return state_ranges

# Randomly generate matrix contain different States type
def generate_random_matrix(num_species, state_ranges):
    """
    Generate a random morphological matrix of character states for a given number of species.

    Args:
        num_species (int): The number of species to generate.
        state_ranges (list): A list of state ranges for each character, where each range
                             is a list of integers representing possible states.

    Returns:
        list: A morphological matrix where each row represents a species,
              with randomly assigned character states.
    """
    # Initialize an empty matrix to store the results
    matrix = []

    # Generate data for each species
    for i in range(num_species):
        species_name = f"SPECIES {i + 1}"  # Create a unique species name
        states = []  # List to store the states for the current species

        # Assign random states for each character
        for states_for_character in state_ranges:
            rand_choice = random.random()  # Generate a random number for probabilistic assignment

            if rand_choice < 0.1:  # 10% chance of missing state
                state = '-'
            elif rand_choice < 0.3:  # 20% chance of multiple states
                state_combination = random.sample(states_for_character, k=random.randint(2, len(states_for_character)))
                state_combination.sort()  # Sort the states for consistency
                state = f"({''.join(map(str, state_combination))})"
            else:  # 70% chance of a single state
                state = str(random.choice(states_for_character))

            states.append(state)  # Append the selected state to the species' states list

        # Append the species name and its states as a row in the matrix
        matrix.append([species_name] + states)

    return matrix

# Show the randomly generated Matrix
def print_matrix(matrix):
    """
    Print the matrix in a readable, tab-delimited format.

    Args:
        matrix (list): The matrix to be printed, where each row is a list of strings.
    """
    for row in matrix:
        print("\t".join(row))

# Parse the character list into state ranges
state_ranges = parse_character_list(character_list_1)

# Print the parsed state ranges for verification
print("Parsed State Ranges:", state_ranges)

# Generate the random matrix
matrix = generate_random_matrix(num_species, state_ranges)

# Print the generated matrix for verification
print("Generated Matrix:")
print_matrix(matrix)

# Function to generate a knowledge graph from a character matrix
def convert_matrix_to_knowledge_graph(matrix):
    """
    Convert a species matrix into a knowledge graph format.

    Args:
        matrix (list): A list where the first element is the species name,
                       followed by character states for that species.

    Returns:
        dict: A dictionary representing the knowledge graph of the species,
              with character names as keys and their corresponding state descriptions as values.
    """
    # Extract the species name from the matrix
    species_name = matrix[0]
    characteristics = {}

    # Process each character state in the matrix
    for i, state in enumerate(matrix[1:], start=1):
        if state == '-':
            # Handle missing states
            characteristics[f"Character{i}"] = "Missing"
        elif state.startswith('(') and state.endswith(')'):
            # Handle multiple states (e.g., "(1,2,3)")
            states = state[1:-1]  # Remove parentheses
            state_desc = " or ".join([f"state {s}" for s in states])
            characteristics[f"Character{i}"] = state_desc
        else:
            # Handle single states
            characteristics[f"Character{i}"] = f"state {state}"

    # Return the knowledge graph as a dictionary
    return {species_name: {"Characteristics": characteristics}}

# Function to call the OpenAI API and generate taxonomic descriptions
def call_api_for_description(knowledge_graph, character_list):
    """
    Generate taxonomic descriptions using OpenAI API based on the knowledge graph and character list.

    Args:
        knowledge_graph (dict): The knowledge graph of a species in JSON-like format.
        character_list (str): The character list in string format.

    Returns:
        str: The generated taxonomic description.
    """
    # Prepare the messages to guide the API in generating descriptions
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

    # Call the OpenAI API to generate the descriptions
    response = client.chat.completions.create(
            model="gpt-4o-2024-08-06",
            messages=messages,
            stop=None,
            temperature=0,
            n=1
        )

    # Extract and return the generated description
    description_content = response.choices[0].message.content
    return description_content

# Global variable to store species descriptions
species_descriptions_dict = {}

def process_species(matrix, character_list):
    """
    Process a morphological matrix to generate taxonomic descriptions for each species.

    Args:
        matrix (list): A list of lists, where each sublist represents a species. The first element is the species name, followed by character states.
        character_list (str): A JSON-like string containing the character list information.

    Returns:
        dict: A dictionary where keys are species names and values are their corresponding taxonomic descriptions.
    """
    global species_descriptions_dict  # Access the global variable to store descriptions
    species_descriptions = {}

    for species_matrix in matrix:
        # Convert the species matrix row to a knowledge graph format
        knowledge_graph = convert_matrix_to_knowledge_graph(species_matrix)

        # Generate taxonomic descriptions using the knowledge graph and character list
        description = call_api_for_description(knowledge_graph,character_list)

        # Extract the species name from the matrix and store the description
        species_name = species_matrix[0]
        species_descriptions[species_name] = description

    # Update the global dictionary with newly processed species descriptions
    species_descriptions_dict.update(species_descriptions)

    return species_descriptions

# Generate species descriptions from the matrix and character list
species_descriptions = process_species(matrix,character_list_1)

# Print the generated species descriptions
print(species_descriptions)

# Prepare messages to guide the generation of a universal character list
messages_character_list = [
    {"role": "system",
     "content": """
     You are a taxonomist specializing in morphological character analysis. 
     The following is a taxonomic description involving multiple species that share a phylogenetic relationship and belong to the same major group.
     Your task is to analyze the descriptions and extract morphological characteristics to generate a universal character list suitable for constructing a character matrix for phylogenetic analysis.
     """},
    {"role": "system",
     "content": """
     When generating the character list, please ensure the following:
     - **Taxonomic Standards**: The character list must conform to biological and taxonomic standards.
     - **Character Independence**: Each character should be independent, describing only one morphological attribute. Avoid combining multiple attributes into a single character.
     - **Character States**: For each character, list all possible states as observed in the descriptions. The states should be discrete and correspond to the relevant description content.
     - **Avoid Quantitative Characters**: Try to avoid selecting quantitative characters (e.g., measurements like length or size). Focus on qualitative characters that are more suitable for phylogenetic analysis.
     - **Shared Derived Characters**: Select characters that are informative for distinguishing among the species in the dataset, focusing on shared derived characters (synapomorphies).
     - **Do not treat missing content as a character state content
     """},
    {"role": "system",
     "content": """
     Please present the character list in the following JSON format:
     ```json
     {
         "1": {
             "description": "Detailed description of Character 1",
             "states": {
                 "1": "Character 1, State 1",
                 "2": "Character 1, State 2"
             }
         },
         "2": {
             "description": "Detailed description of Character 2",
             "states": {
                 "1": "Character 2, State 1",
                 "2": "Character 2, State 2",
                 "3": "Character 2, State 3"
             }
         },
         ...
     }
     ```
     Ensure that the character numbers and state numbers are strings, and the entire output is a valid JSON object.
     """},
    {"role": "user",
     "content": f"""
     Please generate the character list as per the requirements above.
     Here is the combined taxonomic description of all species in the dataset:
     {species_descriptions}
     """}
]

# Generate the universal character list using the OpenAI API
response = client.chat.completions.create(
    model="gpt-4o-2024-08-06",
    messages=messages_character_list,
    stop=None,
    temperature=0,
    n=1
)

# Extract the generated character list from the API response
character_list_2 = response.choices[0].message.content

# Print the generated character list and its type for verification
print(character_list_2)
print(type(character_list_2))
print(type(character_list_1))

# Function to clean the JSON string and remove unnecessary markers
def clean_json_string(json_str: str) -> str:
    """
    Cleans a JSON-like string by removing unnecessary markers and redundant text,
    ensuring it is properly formatted for JSON parsing.

    Args:
        json_str (str): The input string containing JSON content with potential extra markers or text.

    Returns:
        str: A cleaned JSON string ready for parsing.
    """
    # Locate the ```json markers, if present
    json_start_index = json_str.find("```json")
    json_end_index = json_str.rfind("```")

    if json_start_index != -1 and json_end_index != -1:
        # Extract the JSON content between the markers and trim whitespace
        cleaned_str = json_str[json_start_index + len("```json"):json_end_index].strip()
    else:
        # If the markers are not found, clean the entire string
        cleaned_str = json_str.strip()

    # Remove any remaining ```json or ``` markers
    cleaned_str = re.sub(r"```(?:json)?|```", "", cleaned_str, flags=re.MULTILINE).strip()

    return cleaned_str

# Function to parse the character list into a dictionary
def parse_character_list(character_list_str: str) -> Dict:
    """
    Cleans and parses a JSON-like character list string into a dictionary.

    Args:
        character_list_str (str): The input string containing the character list.

    Returns:
        dict: A dictionary representation of the character list.

    Raises:
        ValueError: If the cleaned JSON string is empty or if JSON parsing fails.
    """
    # Clean the input string to remove unnecessary markers and format it as JSON
    cleaned_str = clean_json_string(character_list_str)

    if not cleaned_str:
        # Raise an error if the cleaned string is empty
        raise ValueError("The cleaned JSON string is empty and cannot be parsed.")

    try:
        # Attempt to parse the cleaned string into a dictionary
        character_dict = json.loads(cleaned_str)
    except json.JSONDecodeError as e:
        # Raise a descriptive error if JSON parsing fails
        raise ValueError(f"JSON Parsing Error: {e}")

    return character_dict

# Function to normalize the states for unordered comparison
def normalize_states(states: Dict[str, str]) -> Set[str]:
    """
    Normalize a dictionary of states into a set for unordered comparisons.

    Args:
        states (Dict[str, str]): A dictionary where keys are state IDs and values are state descriptions.

    Returns:
        Set[str]: A set of state descriptions for easy comparison.
    """
    return set(states.values())

# Function to compare two character lists
def compare_character_lists(list1_str: str, list2_str: str) -> Dict:
    """
    Compare two character lists, find differences, and calculate similarity.

    Args:
        list1_str (str): A string representing the first character list.
        list2_str (str): A string representing the second character list.

    Returns:
        dict: A dictionary containing:
            - Summary statistics (total descriptions, matching descriptions, etc.).
            - Detailed comparison results (matching descriptions, missing/different descriptions).
    """
    try:
        # Parse both character lists from their string representation
        list1 = parse_character_list(list1_str)
        list2 = parse_character_list(list2_str)
    except ValueError as e:
        print(f"Parsing Error: {e}")
        return {}
    # Initialize the comparison result structure
    comparison_result = {
        "summary": {},
        "details": {
            "matching_descriptions": [],
            "missing_or_different_descriptions": {}
        }
    }

    # Compare descriptions and states from list1 to list2
    for key1, value1 in list1.items():
        matched_key = None
        for key2, value2 in list2.items():
            # Match descriptions (case-insensitive)
            if value1["description"].lower() == value2["description"].lower():
                matched_key = key2
                comparison_result["details"]["matching_descriptions"].append(value1["description"])
                break

        # Handle unmatched descriptions
        if not matched_key:
            # If no match is found, mark it as a missing description
            comparison_result["details"]["missing_or_different_descriptions"][value1["description"]] = {
                "list1_states": value1["states"],
                "list2_states": "Not found in List 2"
            }
            continue

        # Compare state collections
        states1 = normalize_states(value1["states"])
        states2 = normalize_states(list2[matched_key]["states"])
        if states1 != states2:
            comparison_result["details"]["missing_or_different_descriptions"][value1["description"]] = {
                "list1_states": list(states1),
                "list2_states": list(states2),
                "missing_in_list2": list(states1 - states2),
                "missing_in_list1": list(states2 - states1)
            }

    # Check for descriptions in list2 not present in list1
    for key2, value2 in list2.items():
        if value2["description"].lower() not in \
                (desc.lower() for desc in comparison_result["details"]["matching_descriptions"]):
            comparison_result["details"]["missing_or_different_descriptions"][value2["description"]] = {
                "list1_states": "Not found in List 1",
                "list2_states": value2["states"]
            }

    # Calculate Jaccard similarity coefficient
    all_descriptions = set(value["description"].lower() for value in list1.values()) | \
                       set(value["description"].lower() for value in list2.values())
    common_descriptions = set(value["description"].lower() for value in list1.values()) & \
                          set(value["description"].lower() for value in list2.values())
    jaccard_similarity = len(common_descriptions) / len(all_descriptions)

    # Populate the summary section
    comparison_result["summary"] = {
        "total_descriptions_list1": len(list1),
        "total_descriptions_list2": len(list2),
        "matching_descriptions_count": len(comparison_result["details"]["matching_descriptions"]),
        "different_or_missing_descriptions_count": len(comparison_result["details"]["missing_or_different_descriptions"]),
        "similarity_score": round(jaccard_similarity, 4)
    }

    return comparison_result

# Function to print the comparison results
def print_comparison_result(result: Dict):
    """
    Print the comparison results in a structured and readable format.

    Args:
        result (dict): A dictionary containing the comparison results, including summaries and detailed differences.
    """
    # Print the summary section
    print("\n===== Summary of Comparative Results =====")
    for key, value in result.get("summary", {}).items():
        print(f"{key}: {value}")

    # Print the matching descriptions
    print("\n===== Matching Descriptions =====")
    matching_descriptions = result.get("details", {}).get("matching_descriptions", [])
    if matching_descriptions:
        for desc in matching_descriptions:
            print(f"- {desc}")
    else:
        print("No matching descriptions found.")

    # Print the missing or different descriptions
    print("\n===== Missing or Different Descriptions =====")
    missing_or_different = result.get("details", {}).get("missing_or_different_descriptions", {})
    if missing_or_different:
        for desc, states in missing_or_different.items():
            print(f"\nDescription: {desc}")
            print(f"  List 1 States: {states.get('list1_states', 'N/A')}")
            print(f"  List 2 States: {states.get('list2_states', 'N/A')}")
            if "missing_in_list2" in states:
                print(f"  Exclusive to List 1: {states['missing_in_list2']}")
            if "missing_in_list1" in states:
                print(f"  Exclusive to List 2: {states['missing_in_list1']}")
    else:
        print("No missing or different descriptions found.")

# Perform comparison and print results
result = compare_character_lists(character_list_1, character_list_2)

print_comparison_result(result)








