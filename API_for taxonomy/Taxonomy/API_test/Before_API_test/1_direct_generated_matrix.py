from openai import  OpenAI
import os
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def generate_nexus_content(taxonomy_description, model="gpt-4-turbo"):

    messages = [
        {"role": "system",
         "content": "You are a helpful assistant, skilled in creating NEXUS file formats for phylogenetic analysis."},
        {"role": "user", "content": "I need to convert a taxonomy description into a NEXUS file. Can you help?"},
        {"role": "assistant", "content": "Sure, I can help with that. Please provide the taxonomy description."},
        {"role": "user", "content": taxonomy_description},
        {"role": "user", "content": "For NEXUS format, start with the #NEXUS header."},
        {"role": "user","content": "Follow the NEXUS standards to include the BEGIN DATA block, CHARLABELS, STATELABELS and MATRIX."},
        {"role": "user", "content": "The CHARLABELS show the all character labels in the MATRIX"},
        {"role": "user", "content": "The STATELABELS show the all coded state labels in the MATRIX"},
        {"role": "user", "content": "Create the MATRIX section, listing each species along with their morphological traits."},
        {"role": "user","content": "Ensure the output adheres closely to the structure and requirements of the NEXUS format, especially in the MATRIX section."},
        {"role": "user", "content": "Close the NEXUS file with the 'END;' statement."},
    ]

    response = client.chat.completions.create(model=model,
                                              messages = messages,
                                              max_tokens = 1600,
                                              temperature = 0.3,
                                              stop = ["END;"])
    return response.choices[0].message.content

def process_rtf_and_generate_nexus(text_path, output_path, model="gpt-3.5-turbo"):
    with open(text_path, 'r') as file:
        taxonomy_description = file.read()

    nexus_content = generate_nexus_content(taxonomy_description, model)
    with open(output_path, 'w') as file:
        file.write(nexus_content)
    print(f"NEXUS content saved to {output_path}")


if __name__ == "__main__":
    text_path = "D:/The dataset (contain description, matrix, key)/sampledata (Grass genera(13))/rtf/descrip.txt"  # Replace with your RTF file path
    output_path = "D:/The dataset (contain description, matrix, key)/API_generated_NEXUS/output_file(temperature = 0.33).nex"  # Replace with your desired NEXUS file path
    process_rtf_and_generate_nexus(text_path, output_path)

