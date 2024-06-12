from openai import OpenAI
import os
import json

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

with open("D:/桌面/normalized_matrix_knowledge_graph_22.json", "r") as file:
    matrix_data = json.load(file)
def generate_taxonomic_key(matrix_data):
    matrix_data_str = json.dumps(matrix_data)
    messages = [
        {"role": "system",
         "content":
             "You are a helpful taxonomist assistant." + \
             "You are skilled at calculating the correct information gain to choose the character that best divides species into even groups based on their states." + \
             "Based on the selected character, classify the species into different groups according to their states." + \
             "For each group with more than two species, continue selecting characters to further classify this group until each group only has one species." + \
             "After multiple classifications, determine the final classification levels and record each classifying character and its state. " + \
             "Finally, generate a taxonomic key."},
        {"role": "user", "content":
            "I need to use a morphological matrix to create an accurate classification key. The data is in a JSON file and includes all character states for each species. " + \
            "Select appropriate characters to distinguish the species based on their states. " + \
            "Use information gain to measure the effectiveness of characters. Higher gain means better division of species. " + \
            "Use the dataset to calculate each character's effectiveness. Different numbers represent different states. " + \
            "Don't use characters in order; only consider information gain. I will provide specific steps next."
         },
        {"role": "assistant", "content":
            "Understood. Analyze each character's classification performance using information gain. Higher information gain indicates better classification. Provide the specific steps next."
         },
        {"role": "user", "content":
            "To calculate information gain, follow these steps: " + \
            "1. Calculate the entropy of the entire dataset. The formula for entropy (H) is: " + \
            "   H(S) = -∑(p_i * log2(p_i)), where p_i is the probability of each species. " + \
            "2. For each character, calculate the entropy for each state of the character. " + \
            "3. Calculate the weighted sum of these entropies for each character. " + \
            "4. Subtract this weighted sum from the entropy of the entire dataset to get the information gain for the character. " + \
            "5. Select the character with the highest information gain. " + \
            "Provide the JSON file for the morphological matrix information shortly."
         },
        {"role": "assistant", "content":
            "Understood. Calculate the entropy of the entire dataset, then calculate the entropy for each state of each character, followed by the weighted sum of these entropies. Subtract this weighted sum from the entropy of the entire dataset to get the information gain for each character. Select the character with the highest information gain. Provide the JSON file for the morphological matrix information."
         },
        {"role": "user", "content":
            "Here is the JSON file " + matrix_data_str + ". " + \
            "First, select the initial classification character based on the information gain calculation. " + \
            "It must classify all species and have valid states across all species, not 'Missing' or 'Not Applicable.' " + \
            "Choose characters with fewer than three states. " + \
            "Ignore non-compliant characters and calculate the information gain for the rest. " + \
            "Select the character with the highest information gain and show the information gain values. Provide the selected character and the information gain values for verification."
         },
        {"role": "assistant", "content":
            "Understood. Select the initial classification character with valid states across all species, fewer than three states, and the highest information gain. Show the information gain values for verification. Provide the next steps."
         },
        {"role": "user", "content":
            "When the initial character divides species into subgroups, continue selecting a character for each subgroup if it contains more than two species. " + \
            "Reload the matrix to re-exclude characters with invalid states for those species in the subgroups. " + \
            "If a character is valid for all species in a subgroup, it can be chosen even if it is invalid for some species in other subgroups. " + \
            "Ensure the selected character has valid states for all species within the subgroup. " + \
            "Choose the character with the highest information gain and show the intermediate results and information gain values for each subgroup. Provide the next steps after verification." + \
            "States are represented by numbers. For example, '1,2' means multiple states should be treated as a single state type and this multi-state characterization should not be confused with the individual states within it.The initial character should have no more than three state types."
         },
        {"role": "assistant", "content":
            "Understood. Continue selecting characters for each subgroup, handling invalid states separately. Show the intermediate results and information gain values for verification. Ensure the correct character is chosen for each subgroup. Provide the next steps."
         },
        {"role": "user", "content":
            "Starting with the initial character, classify all species into subgroups based on their states. " + \
            "Progressively subdivide each subgroup using different characters until only one species remains. " + \
            "For subgroups with more than two species, select the character with the highest information gain. " + \
            "Ensure all subgroups are processed, handle invalid states separately, and select the correct character until each subgroup contains only one species. " + \
            "Show the intermediate results for each step to ensure all species are correctly classified. Continue this process until every species is individually classified."
         },
        {"role": "assistant", "content":
            "Understood. Follow the steps, using information gain to select characters and handling invalid states correctly. Show the intermediate results for each step for verification. Ensure each final subgroup contains only one species. Provide the final classification key."
         },
        {"role": "user", "content":
            "Present the results in a nested format, showing how each character and its states divide all species. " + \
            "Construct a taxonomically meaningful and accurate classification key. " + \
            "Show only the results and the information gain values for each character at each stage. " + \
            "Show the result as a dichotomous key format with related information gain." + \
            "Please show the complete result, not only show the example or simplified result, and don't need to show the calculate process only need to show the final result "
         },
        {"role": "assistant", "content":
            "Understood. Construct the classification key using the morphological matrix information, selecting characters based on information gain and handling invalid states. Present all results in a nested structure, showing only the results and the information gain values for the selected characters."
         }
    ]

    response =  client.chat.completions.create(
        model="gpt-4o",
        messages=messages,
        stop=None,
        temperature=0,
        stream =True,
        n = 1,
    )


    for chunk in response:
        if chunk.choices[0].delta.content is not None:
            print(chunk.choices[0].delta.content, end="")

    return chunk.choices[0].delta.content


nexus_content = generate_taxonomic_key(matrix_data)
print(nexus_content)


