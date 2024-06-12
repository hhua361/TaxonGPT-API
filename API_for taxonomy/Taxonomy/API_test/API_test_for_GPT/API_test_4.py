from openai import OpenAI
import os

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def generate_taxonomic_key(matrix, model="gpt-4o"):
    # Message sequence for coding morphological characteristics

    messages = [
        {"role": "system",
         "content": "You are taxonomy assitant, good at to calculate the information gain and building the taxonomic key"},
        # block 1
        {"role": "user", "content": """
            I need to use the morphological matrix of a group of taxa to create an accurate classification key.\n
            The data is in a JSON file and includes all character states for each taxon.\n
            To build the key, appropriate characters must be selected to distinguish the taxa based on their states.\n
            Information gain measures the effectiveness of characters in classification; higher gain means better division of taxa.\n 
            This dataset will be used to calculate each character's effectiveness in distinguishing the taxa.\n
            I will provide specific steps later.
            """},
        {"role": "assistant",
         "content": "Understood. Your main task is to analyze each character's classification performance for different taxa using information gain. Higher information gain indicates a better ability to classify evenly. By progressively selecting characters to narrow down the taxa, you can ultimately construct an accurate classification key. Please provide the specific steps next."},
        # block 2
        {"role": "user", "content": """
                First, select the initial classification character. \n
                This character must classify all taxa and ensure its states are valid across all taxa, not "Missing" or "Not Applicable." \n
                The initial classification character should evenly divide all taxa into several groups based on its states.\n
                To simplify the selection, choose characters with fewer than three states as the initial classification character. \n
                Ignore all non-compliant characters and calculate the information gain for the remaining ones. \n
                Select the character with the highest information gain as the initial classification character.\n
                I will provide the next steps later.
                """},
        {"role": "assistant",
         "content": "Understood. First, select the initial classification character, which must meet the following criteria: no invalid states ('Missing' or 'Not Applicable'), fewer than three states, and the highest information gain among the eligible characters. Please provide the next steps."},
        # block 3
        {"role": "user", "content": """
                When the initial classification character divides all taxa into multiple subgroups based on different states, if a subgroup contains more than two taxa, you need to continue select a classification character for that subgroup.\n
                For each subgroup, handle invalid states separately. \n
                For example, if character X has valid states for all taxa in subgroup 1, it can be chosen as the classification character for subgroup 1, even if it has invalid states in other subgroups.\n
                Ensure the selected classification character has valid states for all taxa within the subgroup. Then, choose the character with the highest information gain for each subgroup.\n
                I will provide the next steps later.
                """},
        {"role": "assistant",
         "content": "Understood. After selecting the initial classification character, you want to continue selecting characters for each resulting subgroup. When selecting classification characters for each subgroup, handle invalid states separately as described to ensure the correct character is chosen for each subgroup."},
        # block 4
        {"role": "user", "content": """
                    Starting with the initial classification character, classify all taxa into different subgroups based on their states. \n
                    Each subgroup is then progressively subdivided using different classification characters until only one taxon remains in each subgroup. \n
                    For subgroups containing more than two taxa, select the character with the highest information gain for further subdivision. \n
                    Ensure that all subgroups are processed, handle invalid states separately, and select the correct character until each subgroup contains only one taxon.\n
                    I will provide the final steps later.
                    """},
        {"role": "assistant",
         "content": "Understood. I will follow the previous steps, using information gain to select classification characters and ensuring invalid states are correctly handled for each subgroup. I will then process each subgroup to ensure that each final subgroup contains only one taxon."},
        # block 5
        {"role": "user", "content": """
                    Please present the results in a nested format, showing how the initial classification character and subsequent characters for each subgroup divide all taxa based on their states. Construct a taxonomically meaningful and accurate classification key. During the analysis, display only the results and the information gain values for each character at each stage.
                    I will provide the JSON file containing the morphological matrix information shortly.
                        """},
        {"role": "assistant",
         "content": "Understood. You want to construct a classification key using the morphological matrix information, selecting appropriate characters based on information gain and correctly handling invalid states. Process each subgroup step-by-step, selecting the appropriate classification character based on information gain. Finally, present all results in a nested structure, showing only the results and the information gain values for the selected classification characters at each step, don't need to show how anaylsis."},
        {"role": "user", "content": f"The morphological matrix information is available in the file with ID: {matrix}"}
    ]

    response =  client.chat.completions.create(
        model=model,
        messages=messages,
        temperature=0,
        stop=None
    )

    return response.choices[0].message.content
def process_rtf_and_generate_nexus(text_path, output_path):
    with open(text_path, 'r') as file:
        matrix = file.read()

        nexus_content = generate_taxonomic_key(matrix)
    with open(output_path, 'w', encoding='utf-8') as file:
            file.write(nexus_content)
if __name__ == "__main__":
    text_path = "D:/桌面/TEST-KG/nexus fix/matrix_knowledge_graph_22.json"
    output_path = "D:/桌面/taxonomy_primary_result/The_API_key_result/2222222/key22.txt"
    process_rtf_and_generate_nexus(text_path, output_path)
