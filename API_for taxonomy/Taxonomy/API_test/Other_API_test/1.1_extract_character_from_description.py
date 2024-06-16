from openai import OpenAI
import os
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def extract_character_and_state(taxonomy_description,character_list,model="gpt-3.5-turbo"):

    messages = [
        {"role": "system","content": "You are a helpful taxonomis assistant, skilled in Extract features from taxonomic descriptions."},
        {"role": "user", "content": "I need to extract the morphological characteristics of a species and its associated state from the taxonomic description. Can you help me?"},
        {"role": "assistant", "content": "Sure, I can help with that. Please provide the taxonomy description."},
        {"role": "user", "content": taxonomy_description},
        {"role": "user", "content": "Start with extract the morphological characteristics of a species and it state"},
        {"role": "user","content": "Collection of morphological characteristics of species, and record the different states of this feature"},
        {"role": "user","content": "Create a list to store these features, and the different states of each feature"},
        {"role": "user","content": "At the same time, I will provide you a character list as the templates"},
        {"role": "user","content": character_list},
        {"role": "user","content": "Please follow this format for the final production"}
    ]
    response = client.chat.completions.create(model=model,
                                              messages = messages,
                                              max_tokens = 1500,
                                              temperature = 0.3,
                                              stop = ["END;"])
    return response.choices[0].message.content

def prompt_and_generate_character_list(text_path,character_path,output_path,model="gpt-3.5-turbo"):
    with open(text_path, 'r') as file:
        taxonomy_description = file.read()
    with open(character_path, 'r') as file:
        character_list = file.read()
    nexus_content = extract_character_and_state(taxonomy_description, character_list, model)
    with open(output_path, 'w') as file:
        file.write(nexus_content)
    print(f"Character list saved to {output_path}")


if __name__ == "__main__":
    text_path = "D:/The dataset (contain description, matrix, key)/sampledata (Grass genera(13))/rtf/descrip.txt"
    character_path = "D:/The dataset (contain description, matrix, key)/sampledata (Grass genera(13))/rtf/chars.txt"
    output_path = "D:/The dataset (contain description, matrix, key)/character_list.txt"
    prompt_and_generate_character_list(text_path, character_path, output_path)