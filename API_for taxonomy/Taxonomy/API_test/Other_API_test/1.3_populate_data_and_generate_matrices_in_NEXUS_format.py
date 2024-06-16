from openai import OpenAI
import os
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def build_the_NEXUS_file(taxonomy_description,character_list,model="gpt-3.5-turbo"):

    messages = [
        {"role": "system","content": "You are a helpful taxonomis assistant, skilled in creating NEXUS file formats matrix"},
        {"role": "user", "content": "I need to convert a taxonomy description into a NEXUS file. Can you help?"},
        {"role": "assistant", "content": "Sure, I can help with that. Please provide the taxonomy description."},
        {"role": "user", "content": taxonomy_description},
        {"role": "user", "content": "I have coded the character list of the species, and the different states of each feature are represented numerically. "},
        {"role": "user", "content": "You should generate NEXUS matrices for these species based on these encoded character. can you help"},
        {"role": "assistant", "content": "Sure, I can help with that. Please provide the coded character list of the species."},
        {"role": "user", "content": character_list},
        {"role": "user", "content": "For each character you can differentially represent the different states of each feature by means of numbers (e.g., 0, 1, 2, 3)."},
        {"role": "user","content": "Morphological features of the species were collected and the different states of each feature were recorded in coded form"},
        {"role": "user", "content": "For NEXUS format, start with the #NEXUS header."},
        {"role": "user","content": "Follow the NEXUS standards to include the BEGIN DATA block, CHARLABELS, STATELABELS and MATRIX."},
        {"role": "user", "content": "The CHARLABELS show the all character labels in the MATRIX"},
        {"role": "user", "content": "The STATELABELS show the all coded state labels in the MATRIX"},
        {"role": "user","content": "Create the MATRIX section, listing each species along with their morphological traits."},
        {"role": "user","content": "Ensure the output adheres closely to the structure and requirements of the NEXUS format, especially in the MATRIX section."},
        {"role": "user", "content": "Close the NEXUS file with the 'END;' statement."},
    ]
    response = client.chat.completions.create(model=model,
                                              messages = messages,
                                              max_tokens = 1500,
                                              temperature = 0.3,
                                              stop = None)
    return response.choices[0].message.content

def prompt_and_generate_character_list(taxonomy_description, character_path,output_path,model="gpt-3.5-turbo"):
    with open(description_path, 'r') as file:
        taxonomy_description = file.read()
    with open(character_path, 'r') as file:
        character_list = file.read()
    nexus_content = build_the_NEXUS_file(taxonomy_description,character_list, model)
    with open(output_path, 'w') as file:
        file.write(nexus_content)
    print(f"Character list (code format) saved to {output_path}")


if __name__ == "__main__":
    description_path = "D:/The dataset (contain description, matrix, key)/sampledata (Grass genera(13))/rtf/descrip.txt"
    character_path = "D:/The dataset (contain description, matrix, key)/character_list.txt"
    output_path = "D:/The dataset (contain description, matrix, key)/output_file.nex"
    prompt_and_generate_character_list(description_path, character_path, output_path)

