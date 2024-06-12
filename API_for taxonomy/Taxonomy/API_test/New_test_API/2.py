from openai import OpenAI
import os

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def process_rtf_and_generate_nexus(text_path, output_path):
    with open(text_path, 'r') as file:
        matrix = file.read()

    initial_result = generate_initial_character(matrix)
    dynamic_result = generate_dynamic_character(initial_result)
    final_result = finalize_classification(dynamic_result, matrix)

    with open(output_path, 'w') as file:
        file.write(final_result)

def generate_initial_character(matrix, model="gpt-4o"):
    messages = [
        {"role": "system", "content": "You are a helpful taxonomic researcher, skilled in calculating the information gain ratio to choose characters and building taxonomic keys."},
        {"role": "user", "content": """
        ### Research aims ###
        • Mission: Construct a taxonomic key using the morphological matrix information of the taxa.
        • Data format: Morphological matrix in JSON format, containing character states for each taxon.
        • Key point: Select classification characters that evenly divide taxa into subgroups with similar numbers.
        • Evaluation: Use information gain ratio to evaluate and select the best classification characters.
        """},
        {"role": "assistant","content": "i know what you what to do and how to do, please provide the specific step and notes"},
        {"role": "user", "content": matrix},
    ]

    response = client.chat.completions.create(
        model=model,
        messages=messages,
        temperature=0,
        max_tokens=1000,
        stop=None
    )

    return response.choices[0].message.content

def generate_dynamic_character(initial_result, model="gpt-4o"):
    messages = [
        {"role": "system", "content": "You are a helpful taxonomic researcher, skilled in calculating the information gain ratio to choose characters and building taxonomic keys."},
        {"role": "user", "content": f"""
        ### Research aims ###
        •Consider the following initial result:
        {initial_result}
        ### Notes ###
        • 'Missing' and 'Not Applicable' statuses are invalid.
        • '1 and 2' state types are multi-state types and should be viewed as separate states.
        • Prefer characters with fewer state types when information gain ratios are equal.
        • Exclude characters with more than 3 state types.
        • Display the final result as a nested structure with numbered levels, retaining character and state information.
        • you don't need to show how to analysis, you need to show the taxonomic keys after analysis
        """},
        {"role": "assistant", "content":"when i doing analysis i will consider this notes, please provide the specific step"},
    ]

    response = client.chat.completions.create(
        model=model,
        messages=messages,
        temperature=0,
        max_tokens=1000,
        stop=None
    )

    return response.choices[0].message.content

def finalize_classification(dynamic_result, matrix, model="gpt-4o"):
    messages = [
        {"role": "system", "content": "You are a helpful taxonomic researcher, skilled in calculating the information gain ratio to choose characters and building taxonomic keys."},
        {"role": "user", "content": f"""
        ### Final Classification ###
        • Based on the dynamic result:
        {dynamic_result}
        ### The process of building a taxonomic key ###
        • Follow these steps:
        1 Select initial character: Ensure it has no invalid status for all taxa; ignore characters with invalid statuses, and choose the highest information gain character, not based on the order
        2 Categorize taxa into subgroups based on the initial character's states.
        3 Select classification characters for each subgroup, reprocessing invalid statuses within each subgroup,for this group don't allow the character has invalid state for the taxon in groups.
        4 Calculate information gain ratio for remaining characters to select the best one for each subgroup.
        5 Repeat: Categorize each subgroup into smaller subgroups, selecting classification characters until all units are uniquely categorized.
        6 show the taxonomic key result
        """},
        {"role": "assistant", "content":"i will follow this step to choose the character and finaly show the correct taxonomic key"},
        {"role": "assistant", "content":"""For example, here has 8 taxon
                                           The character X has the highes information gain ratio and without any invalid states for all taxons;
                                           So the character x be the initial character, and grouped two subgroups ,each subgroup has 4 taxon;
                                           Choose the character Y for subgroups1 to continue classification, and the character Y don't has the invalid state for the taxon in the subgroups1;
                                           At the same time, Choose the character Z for subgroups2 to continue classification, and the character Z don't has the invalid state for the taxon in the subgroups2;
                                           After that, based on above step to continue choose character for the sub-subgroup
                                           until the all taxon can be identified, show the taxonomic key. now please provide the json file, i will not show the analysis process, i will show the taxonomic results after analysis
                                        """},
        {"role": "user", "content": matrix},
    ]

    response = client.chat.completions.create(
        model=model,
        messages=messages,
        temperature=0,
        max_tokens=1000,
        stop=None
    )

    return response.choices[0].message.content

if __name__ == "__main__":
    text_path = "D:/桌面/TEST-KG/nexus fix/matrix_knowledge_graph_22.json"
    output_path = "D:/桌面/taxonomy_primary_result/The_API_key_result/2222222/key22.txt"
    process_rtf_and_generate_nexus(text_path, output_path)
