from openai import OpenAI
import os
import argparse
set.api_key = os.environ['OPENAI_API_KEY']
# Initialize OpenAI client with API key
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
model_use = "gpt-4-turbo"
# Function to extract morphological characteristics and states from taxonomy description
def extract_character_and_state(taxonomy_description,character_list_templates):# ,max_tokens,temperature
        global model_use # Referencing the global variable (though not strictly necessary for reading its value)
        # Message sequence simulates a conversation with the model to guide it on what is expected
        messages = [
            {"role": "system","content": "You are a helpful taxonomis assistant, skilled in Extract features from taxonomic descriptions."},
            {"role": "user","content": "I need to extract the morphological characteristics of a species and its associated state from the taxonomic description. Can you help me?"},
            {"role": "assistant", "content": "Sure, I can help with that. Please provide the taxonomy description."},
            {"role": "user", "content": taxonomy_description},
            {"role": "user","content": "Start with extract the morphological characteristics of a species and it state"},
            {"role": "user","content": "Collection of morphological characteristics of species, and record the different states of this feature"},
            {"role": "user","content": "Create a list to store these features, and the different states of each feature"},
            {"role": "user", "content": "At the same time, I will provide you a character list as the templates"},
            {"role": "user", "content": character_list_templates},
            {"role": "user", "content": "Please follow this format for the final production"}
        ]
        response = client.chat.completions.create(model=model_use,
                                                  messages=messages,
                                                  max_tokens=1600,
                                                  temperature=0.3,
                                                  stop=["END;"])
        return response.choices[0].message.content

# Function to encode the extracted characteristics and states
def encode_character_and_state(character_list):# ,max_tokens,temperature
        global model_use
        # Message sequence for coding morphological characteristics
        messages = [
            {"role": "system", "content": "You are a helpful taxonomis assistant, skilled in Coding Morphological Characteristics."},
            {"role": "user","content": "I have extracted the morphological characteristics of the species and its associated state from the taxonomic description."},
            {"role": "user","content": "Now, I'd like you to translate the states in the Character list I provided into coded form for me, can you help"},
            {"role": "assistant", "content": "Sure, I can help with that. Please provide the character list."},
            {"role": "user", "content": character_list},
            {"role": "user","content": "For each character you can differentially represent the different states of each feature by means of numbers (e.g., 0, 1, 2, 3)."},
            {"role": "user","content": "Morphological features of the species were collected and the different states of each feature were recorded in coded form"},
        ]
        response = client.chat.completions.create(model=model_use,
                                                  messages=messages,
                                                  max_tokens=1600,
                                                  temperature=0.3,
                                                  stop=None)
        return response.choices[0].message.content

# Function to build the NEXUS file from the taxonomy description and encoded character list
def build_the_nexus_file(taxonomy_description,encoded_character_list): # ,max_tokens,temperature
    global model_use
    # Message sequence for generating NEXUS file formats matrix
    messages = [
        {"role": "system","content": "You are a helpful taxonomis assistant, skilled in creating NEXUS file formats matrix"},
        {"role": "user", "content": "I need to convert a taxonomy description into a NEXUS file. Can you help?"},
        {"role": "assistant", "content": "Sure, I can help with that. Please provide the taxonomy description."},
        {"role": "user", "content": taxonomy_description},
        {"role": "user", "content": "I have coded the character list of the species, and the different states of each feature are represented numerically. "},
        {"role": "user", "content": "You should generate NEXUS matrices for these species based on these encoded character. can you help"},
        {"role": "assistant", "content": "Sure, I can help with that. Please provide the coded character list of the species."},
        {"role": "user", "content": encoded_character_list},
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
    response = client.chat.completions.create(model=model_use,
                                              messages = messages,
                                              max_tokens = 1600,
                                              temperature = 0.3,
                                              stop = None)
    return response.choices[0].message.content

# Main function to process taxonomy description to NEXUS file
def process_description_to_NEXUS(description_path, character_path, output_path):
    global model_use # This line is unnecessary for accessing the global variable
    try:
        # Reading the taxonomy description from file
        with open(description_path, 'r') as file:
            taxonomy_description = file.read()
        # Reading the character list templates from file
        with open(character_path, 'r') as file:
            character_list_templates = file.read()
    except IOError as e:
        print(f"Error opening file: {e}")
        return False

    # Extract features and states
    character_list = extract_character_and_state(taxonomy_description,character_list_templates)
    # Coded extracted features
    encoded_character_list = encode_character_and_state(character_list)
    # Construct NEXUS file contents
    nexus_content = build_the_nexus_file(taxonomy_description, encoded_character_list)
    try:
    # Writing the NEXUS content to the specified output file
        with open(output_path, 'w') as file:
            file.write(nexus_content)
        print(f"NEXUS content saved to {output_path}")
        return True
    except IOError as e:
        print(f"Error writing to file: {e}")
        return False

# Execute the main function if the script is run directly
if __name__ == "__main__":
    description_path = "D:/The dataset (contain description, matrix, key)/brithtdata (The Equisetum species (horsetails) 13)/rtf/descrip.txt"
    character_path = "D:/The dataset (contain description, matrix, key)/brithtdata (The Equisetum species (horsetails) 13)/rtf/chars.txt"
    output_path = "D:/The dataset (contain description, matrix, key)/output_file2.nex"
process_description_to_NEXUS(description_path,character_path,output_path)
    # 创建 ArgumentParser 对象
    #parser = argparse.ArgumentParser(description="Process description and characters to generate a NEXUS file.")
    # Add command line arguments
    #parser.add_argument("--description_path", type=str, required=True, help="The file path to the description data.")
    #parser.add_argument("--character_path", type=str, required=True, help="The file path to the character data.")
    #parser.add_argument("--output_path", type=str, required=True, help="The output file path for the NEXUS file.")
    #parser.add_argument("--max_tokens", type=int, default=1500, help="Maximum number of tokens to generate.")
    #parser.add_argument("--temperature", type=float, default=0.3,help="Temperature for controlling the randomness of the generation.")

    # Parse command line arguments
    #args = parser.parse_args()

    #process_description_to_NEXUS(args.description_path, args.character_path, args.output_path,args.max_tokens, args.temperature)