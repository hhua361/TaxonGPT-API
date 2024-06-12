from openai import  OpenAI
import os
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
def generate_taxonomic_key(csv_matrix,model="gpt-4o"):  # ,max_tokens,temperature
    global model_use
    # Message sequence for coding morphological characteristics
    messages = [
        {"role": "user", "content": """
        Generation of Taxonomic key from Morphological Matrix
        I need to generate a taxonomic key using a morphological matrix provided in a CSV file. This matrix contains character states for various taxa. The goal is to determine the characters that best separate the taxa based on their states and progressively categorize them to construct the taxonomic key. The analysis should use information gain to evaluate each character's ability to classify the taxa evenly.
        Please follow these requirements during the analysis:
        1. Initial Character Selection: Ensure all taxa have a defined state ('Missing' or 'Not applicable' is an invalid status) for the first character. Ignore characters with more than two states type and use information gain to select the most suitable character for initial classification.
        2. Dynamic Character Selection: For each new character selection, reload the original matrix. Re-evaluate the presence of invalid states in character, Ignore characters with missing or not applicable states for the current subset of taxa. Include characters with actual states for the taxa being considered, even if they have missing or not applicable states for other taxa.
        3. Character Selection Preference: Prefer characters with fewer state types when multiple characters have the same information gain. Ignore characters with more than three state types regardless of their information gain.
        4. Step-by-Step Classification: Classify taxa step-by-step according to the above rules until all taxa are individually classified. Display the results in a nested structure without showing the code implementation
        """},
        {"role": "assistant",
         "content": "Sure, I can help with that. Please provide the CSV file with the morphological matrix."},
        {"role": "user", "content": csv_matrix}
    ]
    response = client.chat.completions.create(model=model,
                                              messages=messages,
                                              temperature = 0.2,
                                              max_tokens = 1500,
                                              top_p= 1.0,
                                              frequency_penalty=0.8,  # Increase to avoid unnecessary repetition
                                              presence_penalty=0.8,
                                              stop=None)
    return response.choices[0].message.content
def process_rtf_and_generate_nexus(text_path, output_path):

    with open(text_path, 'r') as file:
        csv_matrix = file.read()

    nexus_content = generate_taxonomic_key(csv_matrix)
    with open(output_path, 'w') as file:
        file.write(nexus_content)
    print(f"taxonomic key content saved to {output_path}")

if __name__ == "__main__":
    text_path = "D:/桌面/TEST-KG/nexus fix/processed_data5.csv"  # Replace with your RTF file path
    output_path = "D:/桌面/taxonomy_primary_result/The_API_key_result/2222222/key22.txt"  # Replace with your desired NEXUS file path
    process_rtf_and_generate_nexus(text_path, output_path)