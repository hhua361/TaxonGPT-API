from openai import  OpenAI
import os
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def generate_nexus_content(Nexus_file, model="gpt-4-turbo"):

    messages = [
        {"role": "system",
         "content": "You are a helpful assistant, skilled in based on the NEXUS file to generate the description of each taxons."},
        {"role": "user", "content": "I need to generate taxonomic descriptions for each taxon by recognizing the information extracted from the NEXUS file. Can you help?"},
        {"role": "assistant", "content": "Sure, I can help with that. Please provide the NEXUS file"},
        {"role": "user", "content": Nexus_file},
        {"role": "user", "content": "For NEXUS format, start with the #NEXUS header."},
        {"role": "user","content": "Follow the NEXUS standards to include the BEGIN DATA block, CHARLABELS, STATELABELS and MATRIX."},
        {"role": "user", "content": "The CHARLABELS show the all character labels in the MATRIX"},
        {"role": "user", "content": "The STATELABELS show the all coded state labels in the MATRIX"},
        {"role": "user", "content": "For the matrix part, the column is the character , and the line is the taxon, the number means different state "},
        {"role": "user","content": "Follow the step to generate the taxons description"},
        {"role": "user", "content": "based on this matrix to generate the taxons description, you can first find the character and then know its different state, then you can search the character an its state in the matrix"},
        {"role": "user","content": "i don't need you to show me how you generate the taxons description"},
        {"role": "user", "content": "i want you directly show the taxons description as a paragraph of each taxon"},
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
    output_path = "D:/The dataset (contain description, matrix, key)/API_generated_NEXUS/taxon_description1.txt"  # Replace with your desired NEXUS file path
    process_rtf_and_generate_nexus(matrix_path, output_path)

