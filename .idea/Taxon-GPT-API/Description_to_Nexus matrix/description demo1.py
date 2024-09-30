
import json  # For handling JSON data
from openai import OpenAI  # For interacting with OpenAI API
import os  # For interacting with the operating system, such as file paths
import re  # For regular expressions, useful for pattern matching in strings
import pandas as pd  # For data manipulation and analysis
def load_character_messages(file_path):
    with open(file_path, "r", encoding="utf-8") as file:
        return json.load(file)

# Example Usage
character_file_path = "D:/桌面/Taxonomy_primary_result/The_GPT-4_result/Dataset_3 (The Lycopodiales (Diphasiastrum, Huperzia, Isoetes, Lycopodium, Selaginella)) 4/Information gain methods/character_info_update.json"
character_info = load_character_messages(character_file_path)

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
description = """
1.Diphasiastrum alpinum (L.) Holub
“Alpine Clubmoss”. Lycopodium alpinum L. Morphology. Stems elongated, with numerous small leaves; creeping, and rooting directly at intervals along their length (the erect branches to 10 cm); 15–50(–100) cm long; ostensibly monopodial vegetatively; with only slightly flattened branches; without secondary thickening. Leaves eligulate; strongly 4-ranked on the branches (in alternating, opposite pairs, glaucous); 2–4 mm long; appressed; not hair-pointed. Homosporous. Sporophylls differing markedly from the foliage leaves; aggregated into well defined terminal cones. Cones solitary, sessile at the tips of the normal shoots. The sporangia basal and subsessile on the adaxial surfaces of the sporophylls, non-septate. Ecology and distribution. Lowland, upland and montane (ascending to about 1300 m); moors, montane grassland and mountain tops. Rather common throughout the British Isles, especially at higher elevations. Classification. Family Lycopodiaceae.
"""
messages_initial = [
    {"role": "system",
     "content":
         """
         You are an expert in taxonomic information extraction, skilled in extracting morphological character information from standard taxonomic descriptions based on a given character list.
         The character list specifies different characters and their states for all species in the dataset.
         Please generate a list-form extraction result for each species, listing the state of each trait.
         """},

    {"role": "system",
     "content":
         """
         In the given character list, each character and state has a corresponding number. Please indicate the number for each trait's state in the generated list for each species. If a trait state does not exist, use "Gap" it symbol as '-'.
         After generating the extraction results in list format, please sort the traits and their corresponding states for each species in ascending order, from left to right.
         In the example, the first '1' indicates that character 1 has state number 1 for the species.
         Arrange the list format results accurately as shown in the example.
         For content with multiple feature states use (1,2) to indicate that the CHARACTER has both states of serial number 1, 2.
         """},

    {"role": "system",
     "content":
         """
         To extract character information, follow these steps:
	    • First, check if the species description includes any mention of the character's states. If it does, correctly record the corresponding state label.
	    • If the description does not mention any character states, use your language reasoning skills to strictly check for words indicating the absence of the characteristic (e.g., "non," "no," "not"). If such terms are present, use the corresponding state label based on your reasoning.
        • If there is no mention of the character's states in the species description and your reasoning confirms the absence of relevant content, use "Gap" to represent this.
         """},

    {"role": "user",
     "content": f"Here is species description:{description}"},
    {"role": "user",
     "content": f"Here is character list:{character_info}"}
]

initial_character_info = client.chat.completions.create(
    model="gpt-4o",
    messages=messages_initial,
    stop=None,
    max_tokens=1000,
    temperature=0,
    n=1
)
initial_response = initial_character_info.choices[0].message.content
print(initial_response)


messages_secondary = [
    {"role": "system",
     "content":
         """
         You are an expert in taxonomic information extraction, skilled in extracting morphological character information from standard taxonomic descriptions based on a given character list.
         The character list specifies different characters and their states for all species in the dataset.
         Please generate a list-form extraction result for each species, listing the state of each trait.
         """},

    {"role": "system",
     "content":
         """
         In the given character list, each character and state has a corresponding number. Please indicate the number for each trait's state in the generated list for each species. If a trait state does not exist, use "Gap" it symbol as '-'.
         After generating the extraction results in list format, please sort the traits and their corresponding states for each species in ascending order, from left to right.
         In the example, the first '1' indicates that character 1 has state number 1 for the species.
         Arrange the list format results accurately as shown in the example.
         For content with multiple feature states use (1,2) to indicate that the CHARACTER has both states of serial number 1, 2.
         """},

    {"role": "system",
     "content":
         """
         To extract character information, follow these steps:
	    • First, check if the species description includes any mention of the character's states. If it does, correctly record the corresponding state label.
	    • If the description does not mention any character states, use your language reasoning skills to strictly check for words indicating the absence of the characteristic (e.g., "non," "no," "not"). If such terms are present, use the corresponding state label based on your reasoning.
        • If there is no mention of the character's states in the species description and your reasoning confirms the absence of relevant content, use "Gap" to represent this.
         """},
    {"role": "system",
     "content":
         """
         Sometimes you will ignore some character state, and you need to press this point:
         • If the description does not mention any character states, use your language reasoning skills to strictly check for words indicating the absence of the characteristic (e.g., "non," "no," "not"). If such terms are present, use the corresponding state label based on your reasoning.
         you need to strict to check the "-", which is character state represent the gap, you need to follow the above require to check.
         """},
    {"role": "user",
     "content": f"Here is species description:{initial_response}"},
]

initial_character_info2 = client.chat.completions.create(
    model="gpt-4o",
    messages=messages_secondary,
    stop=None,
    max_tokens=1000,
    temperature=0,
    n=1
)
initial_response2 = initial_character_info.choices[0].message.content
print(initial_response2)
