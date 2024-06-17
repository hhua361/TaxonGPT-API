import json  # For handling JSON data
from openai import OpenAI # For interacting with OpenAI API
import os  # For interacting with the operating system, such as file paths

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def load_prompt_messages(file_path):
    with open(file_path, "r", encoding="utf-8") as file:
        return json.load(file)

def generate_taxonomic_description(species_name, species_data, character_info, prompt_messages):
    # Replace the placeholder in the content template with actual data
    content_with_data = prompt_messages["description_messages"][3]["content_template"].format(
        species_name=species_name,
        species_data=json.dumps(species_data),
        character_info=json.dumps(character_info)
    )

    # Create messages list
    messages = [
        prompt_messages["description_messages"][0],
        prompt_messages["description_messages"][1],
        prompt_messages["description_messages"][2],
        {"role": "user", "content": content_with_data},
        prompt_messages["description_messages"][4]
    ]

    # Make the API call to generate the taxonomic description
    response = client.chat.completions.create(
        model="gpt-4o",
        messages=messages,
        stop=None,
        temperature=0,
        n=1
    )

    # Extract the result from the API response
    result = response.choices[0].message.content
    return result

def main(matrix_file_path, character_info_file_path, output_file_path, prompt_file_path):
    # Read morphological matrix data from a JSON file
    with open(matrix_file_path, "r", encoding="utf-8") as file:
        matrix_data = json.load(file)

    # Read character information data from a JSON file
    with open(character_info_file_path, "r", encoding="utf-8") as file:
        character_info = json.load(file)

    # Load prompt messages from a JSON file
    prompt_messages = load_prompt_messages(prompt_file_path)

    # Output the read data to confirm
    print(matrix_data)
    print(character_info)

    # Create an empty dictionary to store the taxonomic descriptions
    taxonomic_descriptions = {}

    # Iterate over each species and generate taxonomic descriptions
    for species_name, species_data in matrix_data.items():
        description = generate_taxonomic_description(species_name, species_data, character_info, prompt_messages)
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
    prompt_file_path = "D:/桌面/prompt_messages.json"

    # Call the main function with the file paths
    main(matrix_file_path, character_info_file_path, output_file_path, prompt_file_path)
