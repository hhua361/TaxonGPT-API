from openai import  OpenAI
import os
import pandas as pd

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def generate_taxonomic_key(matrix,model="gpt-4o"):  # ,max_tokens,temperature
    global model_use
    # Message sequence for coding morphological characteristics
    messages = [

        {"role": "system", "content": "You are a helpful taxonomis assistant, skilled in calculate the gain ratio to choose character then building the classification classification key"},
        {"role": "user","content": "I need to generate a taxonomic key using a morphological matrix provided in a csv file. This matrix contains character states for various taxa. The goal is to determine the characters that best separate the taxa based on their states and progressively choose the character to construct the classification key. The analysis should use information gain ratio, GR to evaluate each character's ability to classify the taxa evenly."},
        {"role": "assistant", "content": "Sure, I will choose the suitable character for the different taxa group based on the information gain ratio, GR and generate the classification key for you."},
        {"role": "user","content": "Please follow these requirements during the analysis:"},
        {"role": "user","content": "1. Initial Character Selection: Ensure all taxa have a valid state ('Missing' or 'Not Applicable' is an invalid states) for the initial character. Ignore characters with more than three states type (mulitiple state('1,2') can as a state type) and use information gain ratio, GR to select the most suitable character for initial classification."},
        {"role": "assistant","content": "Sure,For the initial character selection, you want all taxas to valid states about this character ('Missing' or 'Not Applicable' is an invalid states) and only two states exist for these characters, and subsequently I need to compute information gain ratio, GR on each of the remaining characters to determine which character to use as the first categorized character ."},
        {"role": "user","content": "2. Dynamic Character Selection: For each new character selection, reload the original matrix. Re-evaluate the presence of invalid states in character, Ignore characters with ’missing‘ or ‘Not Applicable’ states for the current subset of taxa. Include characters with valid states for the taxa being considered, even if they have 'Missing' or 'Not applicable' states for other taxa, (This point is very important.)"},
        {"role": "assistant","content": "Sure, I understand what you mean, this is very important. You are saying that when selecting the initial character, you need to first filter out those characters that have invalid states for all taxa (such as 'Missing' or 'Not Applicable') and characters that have more than three states. Therefore, if you continue to use these character lists, subsequent character selection will be incorrect. Therefore, we need to reload the entire matrix data to ensure that when classifying each subgroup divided by the initial character, the correct character can be selected for further classification. Just make sure that this character does not have an invalid states in the group that currently needs to be classified."},
        {"role": "user","content": "3. Character Selection Preference: Prefer characters with fewer state types when multiple characters have the same information gain ratio, GR. Ignore characters with more than three state types regardless of their information gain ratio, GR."},
        {"role": "assistant", "content": "Of course I understand that the calculation method of information gain ratio, GR will prefer to select characters with multiple state types. Therefore, when multiple characters have the same information gain ratio, GR, the character with fewer state types is preferred; and when the state types exceed If there are more than three types, I will directly ignore this character, no matter how high its information gain ratio, GR is."},
        {"role": "user","content": "4. Some of the characters in the matrix have states “1,2” which means that both state1 and state2 exist for this character,so '1,2' should be considered as a separate state."},
        {"role": "assistant","content": "Sure, I will make sure to deal with the mulitple such as state 1,2 correctly for each character."},
        {"role": "user","content": "5. Step-by-Step Classification: Classify taxa step-by-step according to the above rules until all taxa are individually classified (each taxa should be divide no subgroup). Display the results in a nested structure without showing the code implementation"},
        {"role": "assistant","content": "Of course, I understand that there is multi-state information in this matrix, e.g. '1,2' means that a certain taxa has both state1 and state2 of a certain character. at the same time, all multi-featured states should be considered as one state type."},
        {"role": "user", "content": "Here's a morphological matrix in csv format:"},
        {"role": "user", "content": matrix},
        {"role": "assistant", "content": "I will not ignore any taxa. I will first choose the initial character and then, for each subgroup divided by the initial character, reload the character matrix information. I will ignore characters with invalid states for the taxa in the current subgroup and, based on information gain ratio, GR, choose the appropriate character. This process will continue until all taxa are individually classified. It is important to note that if a character has valid states for the taxa in the current subgroup but invalid states for other taxa, this character should still be considered."},
    ]

    #for message in messages:
        #print("Message:", message)

    response = client.chat.completions.create(model=model,
                                              messages=messages,
                                              stop=None)
    #print("Response:", response)

    return response.choices[0].message.content
def process_rtf_and_generate_nexus(text_path, output_path):
    with open(text_path, 'r') as file:
        matrix = file.read()
    #print("CSV Matrix Content:\n", csv_matrix)
    nexus_content = generate_taxonomic_key(matrix)
    with open(output_path, 'w') as file:
        file.write(nexus_content)

if __name__ == "__main__":
    text_path = "D:/桌面/TEST-KG/nexus fix/processed_data5.csv" # Replace with your RTF file path
    output_path = "D:/桌面/taxonomy_primary_result/The_API_key_result/2222222/key22.txt"  # Replace with your desired NEXUS file path
    process_rtf_and_generate_nexus(text_path, output_path)

# csv path: "D:/桌面/taxonomy_primary_result/The_GPT-4_result/Dataset_3 (The Lycopodiales (Diphasiastrum, Huperzia, Isoetes, Lycopodium, Selaginella)) 4/Information gain methods/process_data.csv"
# store path: "D:/桌面/taxonomy_primary_result/The_API_key_result/2222222/key.txt"