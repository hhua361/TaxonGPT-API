from openai import  OpenAI
import os

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
def process_rtf_and_generate_nexus(text_path, output_path):
    with open(text_path, 'r') as file:
        matrix = file.read()

    initial_result = generate_initial_character(matrix)
    dynamic_result = generate_dynamic_character(initial_result)
    final_result = finalize_classification(dynamic_result,initial_result, matrix)

    with open(output_path, 'w') as file:
        file.write(final_result)
def generate_initial_character(matrix, model="gpt-4o"):
    messages = [
        {"role": "system",
         "content": "You are a helpful taxonomist assistant, skilled in calculating the gain ratio to choose characters and building classification keys."},
        {"role": "user", "content": """
        ### Research aims###
	    • Missions: You need to construct a taxonomic key by using the morphological matrix information of the taxon.
	    • Data format: The taxon's morphological matrix information is stored in a knowledge graph in JSON format, which contains information about the state of each taxon with respect to different characters. (don't need to show the matrix)
	    • Key point: The key to building a correct taxonomic key is to gradually select suitble classification characters. The suitble classification characters need to be able to evenly divide taxa into several subgroups, and each subgroup needs to have a relatively uniform number of taxons.
        • Evaluate method: By calculating each character based on the information gain ratio, the ability of each character to be classified uniformly is evaluated to select the character with the highest information gain ratio for classification.
        """},
        {"role": "assistant",
         "content": "Sure, I will follow these guidelines to select the suitable characters based on the information gain ratio (GR) and generate the taxonomic key, and please provide the follow requirment, i will not show the code about how i analysis, i will directly show you result"},
        {"role": "user", "content": matrix},
    ]

    response = client.chat.completions.create(
        model=model,
        messages=messages,
        temperature=0,
        max_tokens=3000,
        stop=None
    )

    return response.choices[0].message.content


def generate_dynamic_character(initial_result, model="gpt-4o"):
    messages = [
        {"role": "system",
         "content": "You are a helpful taxonomist assistant, skilled in calculating the gain ratio to choose characters and building classification keys."},
        {"role": "user", "content": f"""
            At the same time consider ### Research aims ###:
            {initial_result}
        ### Notes ###
	    • In morphological matrix, 'Missing' and 'Not Applicable' are invalid statuses and have no categorical significance.
	    • There are '1 and 2' state types in the morphological matrix, and states connected using 'and' are denoted as multi-state types, meaning that for this character both state1 and state2 exist, and each multi-state type should be viewed as a separate state type.
	    • In the information gain ratio calculation process, there will be multiple characters with the same information gain ratio level, and the character with fewer state types will be preferred.
	    • Characters with more than 3 state types are not used to selectively build a taxonomic key.
        • The final result should be displayed as a nested structure, with numbers indicating the levels of the nested structure, while also retaining character and state information.
        • Please don't show you how to analysis, show me the final taxonomic key results.
        """},
        {"role": "assistant",
         "content": "Sure, when i choose the character and build the taxonomic key i will mention this note, and i will not show the analysis process i will directly provide result"},
    ]

    response = client.chat.completions.create(
        model=model,
        messages=messages,
        temperature=0,
        max_tokens=3000,
        stop=None
    )

    return response.choices[0].message.content


def finalize_classification(dynamic_result,initial_result,matrix, model="gpt-4o"):
    messages = [
        {"role": "system",
         "content": "You are a helpful taxonomist assistant, skilled in calculating the gain ratio to choose characters and building classification keys."},
        {"role": "user", "content": "f'At same times consider {dynamic_result}"},
        {"role": "user", "content":"""
        ### The process of building a taxonomic key ###
            • Select initial classification character: Since the initial character needs to be guaranteed to classify all taxons, it is necessary to ensure that the selected initial classification character does not have any invalid status for all taxons, that is, characters that have invalid status for all taxons are ignored before selection.
            • After selecting the initial classification character, all taxon are categorized into several subgroups based on the different states of the initial classification character.
            • Further select classification characters for the taxon in each subgroup.
            • When selecting characters for each subgroup, you need to reprocess the invalid status. Since the subgroup only contains part of the taxon, when selecting the classification character for each subgroup, you only need to ignore the characters whose taxon has an invalid status in the current subgroup.
            • After processing the invalid states, the information gain ratio is calculated for the remaining characters in each subgroup to select the highest character as the categorized character.
            • Repeat the categorization process: For each subgroup, it is further categorized into smaller subgroups (subsubgroups) based on selected classification features.
            • Select categorization character for each new subgroup as described above.
            • Continue this process until all classification units are individually categorized and have a unique classification path pointing to each classification unit.
            • Please directly show the taxonomic key result"""},
        {"role": "assistant", "content": "Sure, I know the whole process of building a taxonomic key and the realted notes and i will not show the code about how i analysis, i will directly show you result. Please provide the JSON file with the morphological matrix."},
        {"role": "user", "content": matrix},
    ]

    response = client.chat.completions.create(
        model=model,
        messages=messages,
        temperature=0,
        max_tokens=3000,
        stop=None
    )

    return response.choices[0].message.content


if __name__ == "__main__":
    text_path = "D:/桌面/TEST-KG/nexus fix/matrix_knowledge_graph_22.json"  # 替换为你的CSV文件路径
    output_path = "D:/桌面/taxonomy_primary_result/The_API_key_result/2222222/key22.txt"  # 替换为你想保存的路径
    process_rtf_and_generate_nexus(text_path, output_path)
