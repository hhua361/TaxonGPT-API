from openai import OpenAI
import os
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
def encode_character_and_state(character_list,model="gpt-3.5-turbo"):

    messages = [
        {"role": "system","content": "You are a helpful taxonomis assistant, skilled in Coding Morphological Characteristics."},
        {"role": "user", "content": "I have extracted the morphological characteristics of the species and its associated state from the taxonomic description."},
        {"role": "user", "content": "Now, I'd like you to translate the states in the Character list I provided into coded form for me, can you help"},
        {"role": "assistant", "content": "Sure, I can help with that. Please provide the character list."},
        {"role": "user", "content": character_list},
        {"role": "user", "content": "For each character you can differentially represent the different states of each feature by means of numbers (e.g., 0, 1, 2, 3)."},
        {"role": "user","content": "Morphological features of the species were collected and the different states of each feature were recorded in coded form"},
    ]
    response = client.chat.completions.create(model=model,
                                              messages = messages,
                                              max_tokens = 1500,
                                              temperature = 0.3,
                                              stop = None)
    return response.choices[0].message.content
def prompt_and_generate_character_list(character_path,output_path,model="gpt-3.5-turbo"):
    with open(character_path, 'r') as file:
        character_list = file.read()
    nexus_content = encode_character_and_state(character_list, model)
    with open(output_path, 'w') as file:
        file.write(nexus_content)
    print(f"Character list (code format) saved to {output_path}")


if __name__ == "__main__":
    character_path = "D:/The dataset (contain description, matrix, key)/sampledata (Grass genera(13))/rtf/chars.txt"
    output_path = "D:/The dataset (contain description, matrix, key)/character_list.txt"
    prompt_and_generate_character_list(character_path, output_path)