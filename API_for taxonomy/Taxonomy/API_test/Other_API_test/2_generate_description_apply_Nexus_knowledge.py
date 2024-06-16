from openai import  OpenAI
import os
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def generate_nexus_content(Nexus_file, model="gpt-4-turbo"):

    messages = [
        {"role": "system",
         "content": "You are a helpful assistant, skilled in based on the NEXUS file to generate the description of each taxons."},
        {"role": "user", "content": "I want you transfer the morphological matrix to the taxon description."},
        {"role": "user", "content": "I will provide you with a morphological matrix in a NEXUS file."},
        {"role": "assistant", "content": "Sure, I can help with that. Please provide the NEXUS file"},
        {"role": "user", "content": Nexus_file},
        {"role": "user", "content": "A NEXUS file,  containsfile, contains CHARLABELS, STATELABELS, MATRIX blocks."},
        {"role": "user","content": "In the CHARLABELS, it shows all the morphological characters that occur in these tax and matrix."},
        {"role": "user", "content": "In the STATELABELS, It shows the different character states corresponding to each character."},
        {"role": "user", "content": "In the MATRIX, It shows the character states that each species possessesfor all characters., Missing characters are denoted by '?' and GAP is denoted by '-'.When a taxon has many states for a given character,  all states are included within parentheses, i.e., (). For instance, (123) indicates that a particular taxon has character states 1, 2 and 3 for a given character.  For any given character, if a taxon does not have a particular character state, or the information about the character state is missing, the NEXUS matrix will put a “?” or “-“ in its place.  This indicates that there is no information about that character state, and that character state should not be included in the description for that taxon."},
        {"role": "user", "content": "When I provide you a Nexus file, you should follow these steps to generate an  accuratean accurate taxonomic description of all taxa in the file. "},
        {"role": "user","content": "First you should use the CHARLABELS and STATELABELS blocks, to find the characters and their corresponding states."},
        {"role": "user", "content": "For the matrix, each row represents a taxon, and each column represents a character.  For each taxon row, character states are represented sequentially as numbers corresponding to the numbers specified in STATELABELS. "},
        {"role": "user","content": "So, you should check the matrix, and based on the character state in each row of  the matrix, generate the taxon description. Do this for all rows in the matrix to generate a complete taxonomic description of all taxa. "},
        {"role": "user", "content": "For generated descriptions, you should use the academic language of taxonomy, and avoid the use of superfluous adjectives, etc."},
    ]


    response = client.chat.completions.create(model=model,
                                              messages = messages,
                                              max_tokens = 4096,
                                              temperature = 0.1,
                                              stop = ["END;"])
    return response.choices[0].message.content

def process_rtf_and_generate_nexus(matrix_path, output_path, model="gpt-3.5-turbo"):
    with open(matrix_path, 'r',encoding='windows-1252') as file:
        Nexus_file = file.read()

    taxon_description = generate_nexus_content(Nexus_file, model)
    with open(output_path, 'w') as file:
        file.write(taxon_description)
    print(f"taxon description saved to {output_path}")


if __name__ == "__main__":
    matrix_path = "D:/桌面/taxonomy_primary_result/The_GPT-4_result/Dataset_2 (The Equisetum species (horsetails)) 3/DELTA_data/nexdata"
    output_path = "D:/The dataset (contain description, matrix, key)/API_generated_NEXUS/taxon_description2.txt"  # Replace with your desired NEXUS file path
    process_rtf_and_generate_nexus(matrix_path, output_path)

