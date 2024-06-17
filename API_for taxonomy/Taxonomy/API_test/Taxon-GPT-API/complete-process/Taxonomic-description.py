import json  # For handling JSON data
from openai import OpenAI  # For interacting with OpenAI API
import os  # For interacting with the operating system, such as file paths

# Set the OpenAI API key
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))


def generate_taxonomic_description(species_name, species_data, character_info):
    messages_desctiption = [
        {"role": "system","content": """
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
        {"role": "assistant", "content":"""
            Sure, I know how to generate a taxonomic description, and I will handle the multiple states in the description.
            I will follow these specific requirements:
            1. Generate standard academic taxonomic descriptions strictly corresponding to the morphological matrix and eigenstate information.
            2. For the generated taxonomy descriptions, I will generate separate descriptions in list form and paragraph form.
            """},
        {"role": "user", "content":f"""
            Due to the large number of results, to avoid space constraints, please show the taxonomic description of each taxon separately.
            Here is the morphological matrix for species {species_name}: {json.dumps(species_data)}.
            Here is the character info: {json.dumps(character_info)}.
            """},
        {"role": "assistant", "content":"I will step by step show the taxonomic description results."}
    ]

    # Make the API call to generate the taxonomic description
    response = client.chat.completions.create(
        model="gpt-4o",
        messages=messages_desctiption,
        stop=None,
        temperature=0,
        n=1
    )

    # Extract the result from the API response
    result = response.choices[0].message.content
    return result


def main(matrix_file_path, character_info_file_path, output_file_path):
    # Read morphological matrix data from a JSON file
    with open(matrix_file_path, "r", encoding="utf-8") as file:
        matrix_data = json.load(file)

    # Read character information data from a JSON file
    with open(character_info_file_path, "r", encoding="utf-8") as file:
        character_info = json.load(file)

    # Output the read data to confirm
    print(matrix_data)
    print(character_info)

    # Create an empty dictionary to store the taxonomic descriptions
    taxonomic_descriptions = {}

    # Iterate over each species and generate taxonomic descriptions
    for species_name, species_data in matrix_data.items():
        description = generate_taxonomic_description(species_name, species_data, character_info)
        taxonomic_descriptions[species_name] = description

    # Write the results to a file
    with open(output_file_path, 'w', encoding='utf-8') as f:
        json.dump(taxonomic_descriptions, f, ensure_ascii=False, indent=4)

    print(f"Taxonomic descriptions have been generated and saved to '{output_file_path}'.")

if __name__ == "__main__":
    # Define file paths
    matrix_file_path = "D:/桌面/TEST-KG/nexus fix/matrix_knowledge_graph_22.json"
    character_info_file_path = "D:/桌面/TEST-KG/nexus fix/updated_character_info.json"
    output_file_path = "D:/桌面/taxonomic_descriptions.json"

    # Call the main function with the file paths
    main(matrix_file_path, character_info_file_path, output_file_path)
