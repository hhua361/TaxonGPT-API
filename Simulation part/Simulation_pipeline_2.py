import json
from openai import OpenAI
import os
import random
import re
import pandas as pd

# input the original taxonomic description as the first input for the generated character list
The_original_description = """
Ameletus Eaton
Imago. The compound eyes contiguous (in males), or widely separated (in females); rounded. Fore-wings with R5 and R4 joined basally. Hind-wings present. The hind-wings of the female imagines more than one fifth the length of the fore-wings. Hind tarsi slightly shorter than the tibia. Hind tarsi with 4 moveable segments. The hind tarsal claws unalike, being one pointed and one blunt. The abdomen with two tails. Male claspers separate. Nymph. The outer tails hairy on the inner side only. Gills mostly at the sides of the abdomen; not fringed with filaments on both sides. Classification. Superfamily Heptagenioidea. Family Siphlonuridae. British representation. 1 species (A. inopinatus).

Baetis Leach
Imago. The compound eyes distinctly two-lobed (in males), or rounded (in females); upper lobe in the males, turbanate. Fore-wings with R5 detached basally from R4. The marginal fore-wing veinlets paired. Hind-wings present. The hind-wings of the female imagines no more than one fifth the length of the fore-wings. The hind-wing costa smoothly curved, or with a conspicuous projection. Hind tarsi with 4 moveable segments, or with 2–3 moveable segments (?). The abdomen with two tails. Nymph. The outer tails hairy on the inner side only. Gills mostly at the sides of the abdomen; not fringed with filaments on both sides; never comprising a plate bearing a tuft of filaments. Classification. Superfamily Baetoidea. Family Baetidae. British representation. 9 species; B. atrebatinus (Dark Olive Dun and Spinner), B. buceratus, B. digitatus, B. fuscatus (Pale Watery Dun and male Spinner, Golden Spinner female), B. muticus (Iron Blue Dun, Iron Blue or Jenny Spinner male, and Little Claret female Spinner), B. niger, B. rhodani (Large Dark Olive Dun and male Spinner, Large Red female Spinner), B. scambus Small Dark Olive Dun and male Spinner, (Small Red female Spinner), and B. vernus (Medium Olive Dun and male Spinner, Red Spinner female).

Brachycercus Curtis
Eurycaenis Bengtsson. Imago. The compound eyes rounded. Second antennal segment three times as long as the first. Wings fringed in the imago. Fore-wings with R5 and R4 joined basally. Hind-wings absent. The fore-legs widely separated under the thorax. Hind tarsi with 4 moveable segments. The abdomen with three tails. Nymph. Gills mostly lying on the upper surface of the abdomen; not fringed with filaments on both sides. Classification. Superfamily Baetoidea. Family Caenidae. British representation. 1 species (B. harrisella).

Caenis Stephens
Ordella Campion. Imago. The compound eyes rounded. Second antennal segment no more than twice as long as the first. Wings fringed in the imago. Fore-wings with R5 and R4 joined basally. Hind-wings absent. The fore-legs inserted relatively close together under the thorax. Hind tarsi with 4 moveable segments. The abdomen with three tails. Nymph. Gills mostly lying on the upper surface of the abdomen; not fringed with filaments on both sides. Classification. Superfamily Baetoidea. Family Caenidae. British representation. 5 species; C. horaria, C. luctuosa, C. macrura, C. rivulorum, C. robusta (all the Duns and Spinners colloquially named Angler’s Curse).

Centroptilum Eaton
Imago. The compound eyes distinctly two-lobed (in males), or rounded (in females); upper lobe in the males, turbanate. Fore-wings with R5 detached basally from R4. The marginal fore-wing veinlets single. Hind-wings present. The hind-wings of the female imagines no more than one fifth the length of the fore-wings. The hind-wing costa with a conspicuous projection. Hind tarsi with 4 moveable segments, or with 2–3 moveable segments (?). The abdomen with two tails. Nymph. The outer tails hairy on the inner side only. Gills mostly at the sides of the abdomen; not fringed with filaments on both sides. Classification. Superfamily Baetoidea. Family Baetidae. British representation. 2 species; C. luteolum (Small Spurwing or Pale Watery Dun, Small Spurwing male Spinner, and Little Amber female Spinner), and C. pennulatum (Large Spurwing Dun and male Spinner, Large Amber female Spinner).

Cloeon Leach
Imago. The compound eyes rounded. Fore-wings with R5 detached basally from R4. Hind-wings absent. The hind-wings of the female imagines more than one fifth the length of the fore-wings. Hind tarsi with 4 moveable segments. The first segment of the hind tarsus about twice as long as the second. The abdomen with two tails. Nymph. The outer tails hairy on the inner side only. Gills mostly at the sides of the abdomen; not fringed with filaments on both sides. Classification. Superfamily Baetoidea. Family Baetidae. British representation. 2 species; C. dipterum (Pond Olive or Lake Olive Dun, Pond Olive male Spinner, Apricot Spinner female), and C. simile.

Ecdyonurus Eaton
Ecdyurus Eaton. Imago. The compound eyes contiguous (in males), or widely separated (in females); rounded. Wings more or less spotted with brown or blackish. Fore-wings with R5 and R4 joined basally. Hind-wings present. The hind-wings of the female imagines more than one fifth the length of the fore-wings. Hind tarsi with 5 moveable segments. The hind tarsal claws unalike, being one pointed and one blunt. The abdomen with two tails. Male claspers crossed. The lobes of the penis very broad-tipped, and closely approximated. Nymph. Gills mostly at the sides of the abdomen; not fringed with filaments on both sides; mostly consisting of a plate bearing a tuft of filaments. Classification. Superfamily Heptagenioidea. Family Heptageniidae. British representation. 4 species; E. dispar (Autumn or August Dun, Autumn or Red Spinners), E. insignis (Large Green Dun and Spinners), E. torrentis (Large Brook Dun and Spinners, or Great Red Spinner), and E. venosus (Late March Brown Dun and Spinners, or Great Red Spinner).

Ephemera Linnaeus
Imago. The compound eyes rounded. Wings more or less spotted with brown or blackish. Fore-wings with veins M1 and Cu1 strongly strongly diverging basally; with R5 and R4 joined basally. Hind-wings present. The hind-wing costa smoothly curved. Hind tarsi with 4 moveable segments, or with 2–3 moveable segments. The abdomen with three tails. The lobes of the penis without recurved appendages. Nymph. Gills all densely fringed with filaments on both sides. Classification. Superfamily Ephemeroidea. Family Ephemeridae. British representation. 3 species; E. danica (Mayfly or Green Drake Dun, Mayfly male Spinner, and Mayfly, Spent Gnat or Black Drake female Spinner), E. lineata, and E. vulgata (Drake Mackerel Dun and Spinners).

Ephemerella Walsh
Imago. The compound eyes rounded. Fore-wings with R5 and R4 joined basally. Hind-wings present. The hind-wing costa smoothly curved. Hind tarsi with 4 moveable segments. The abdomen with three tails. The lobes of the penis without recurved appendages. Nymph. Gills mostly lying on the upper surface of the abdomen; not fringed with filaments on both sides. Classification. Superfamily Baetoidea. Family Ephemerellidae. British representation. 2 species; E. ignita (Blue Winged Olive or B.W.O. Dun and male Spinner, Sherry Spinner female), and E. notata (Yellow Evening Dun and Spinners).

Habrophlebia Eaton
Imago. The compound eyes distinctly two-lobed (in males), or rounded (in females); upper lobe in the males rounded. Fore-wings with R5 and R4 joined basally. Hind-wings present. The hind-wing costa with a conspicuous projection. Hind tarsi with 4 moveable segments. The abdomen with three tails. Nymph. The outer tails hairy on both sides. Gills mostly at the sides of the abdomen; not fringed with filaments on both sides; never comprising a plate bearing a tuft of filaments. Classification. Superfamily Baetoidea. Family Leptophlebiidae. British representation. 1 species; H. fusca (Ditch Dun and Spinners).

Heptagenia Walsh
Imago. The compound eyes widely separated; rounded. Fore-wings with R5 and R4 joined basally. Hind-wings present. The hind-wings of the female imagines more than one fifth the length of the fore-wings. Hind tarsi with 5 moveable segments. The hind tarsal claws unalike, being one pointed and one blunt. The abdomen with two tails. The lobes of the penis without recurved appendages. Nymph. Gills mostly at the sides of the abdomen; not fringed with filaments on both sides; mostly consisting of a plate bearing a tuft of filaments. Classification. Superfamily Heptagenioidea. Family Heptageniidae. British representation. 4 species; H. fuscogrisea (Brown May Dun and Spinners), H. lateralis (Dusky Yellowstreak or Dark Dun, Dusky Yellowstreak Spinners), H. longicauda, and H. sulphurea (Yellow May Dun and Spinners).

Leptophlebia Westwood
Imago. The compound eyes distinctly two-lobed (in males), or rounded (in females); upper lobe in the males rounded. Fore-wings with R5 and R4 joined basally. Hind-wings present. The hind-wing costa smoothly curved. Hind tarsi with 4 moveable segments. The abdomen with three tails. The lobes of the penis each with one recurved appendage. Nymph. The outer tails hairy on both sides. Gills mostly at the sides of the abdomen; not fringed with filaments on both sides; never comprising a plate bearing a tuft of filaments. Classification. Superfamily Baetoidea. Family Leptophlebiidae. British representation. 2 species; L. marginata (Sepia Dun and Spinners), and L. vespertina (Claret Dun and Spinners).

Paraleptophlebia Lestage
Imago. The compound eyes distinctly two-lobed (in males), or rounded (in females); upper lobe in the males rounded. Fore-wings with R5 and R4 joined basally. Hind-wings present. The hind-wing costa smoothly curved. Hind tarsi with 4 moveable segments. The abdomen with three tails. The lobes of the penis each with two recurved appendages. Nymph. The outer tails hairy on both sides. Gills mostly at the sides of the abdomen; not fringed with filaments on both sides; never comprising a plate bearing a tuft of filaments. Classification. Superfamily Baetoidea. Family Leptophlebiidae. British representation. 3 species; P. cincta (Purple Dun and Spinners), P. submarginata (Turkey Brown Dun and Spinners), and P. werneri.

Potamanthus Pictet
Imago. The compound eyes rounded. Wings unspotted. Fore-wings with veins M1 and Cu1 strongly strongly diverging basally; with R5 and R4 joined basally. Hind-wings present. Hind tarsi with 4 moveable segments, or with 2–3 moveable segments. The abdomen with three tails. Nymph. Gills all densely fringed with filaments on both sides. Classification. Superfamily Ephemeroidea. Family Potamanthidae. British representation. 1 species (P. luteus).

Procloeon Bengtsson
Imago. The compound eyes rounded. Fore-wings with R5 detached basally from R4. Hind-wings absent. The hind-wings of the female imagines more than one fifth the length of the fore-wings. Hind tarsi with 4 moveable segments. The first segment of the hind tarsus about three times as long as the second. The abdomen with two tails. Nymph. The outer tails hairy on the inner side only. Gills mostly at the sides of the abdomen; not fringed with filaments on both sides. Classification. Superfamily Baetoidea. Family Baetidae. British representation. 1 species; P. bifidum (Pale Evening or Pale Watery Dun, Pale Evening Spinners).

Rhithrogena Eaton
Imago. The compound eyes contiguous (in males), or widely separated (in females); rounded. Fore-wings with R5 and R4 joined basally. Hind-wings present. The hind-wings of the female imagines more than one fifth the length of the fore-wings. Hind tarsi with 5 moveable segments. The hind tarsal claws unalike, being one pointed and one blunt. The abdomen with two tails. Male claspers crossed. The lobes of the penis narrow, rod-shaped, and widely separated; without recurved appendages. Nymph. Gills mostly at the sides of the abdomen; not fringed with filaments on both sides; mostly consisting of a plate bearing a tuft of filaments. Classification. Superfamily Heptagenioidea. Family Heptageniidae. British representation. 2 species; R. germanica (March Brown Dun, March Brown or Great Red Spinner), and R. semicolorata (Olive Upright Dun, Yellow Upright Spinners).

Siphlonurus Eaton
Siphlurella Bengtsson, Siphlurus Eaton. Imago. The compound eyes rounded. Fore-wings with R5 and R4 joined basally. Hind-wings present. The hind-wings of the female imagines more than one fifth the length of the fore-wings. Hind tarsi about one-and-a-half times the length of the tibia. Hind tarsi with 4 moveable segments. The hind tarsal claws both pointed. The abdomen with two tails. Nymph. The outer tails hairy on the inner side only. Gills mostly at the sides of the abdomen; not fringed with filaments on both sides. Classification. Superfamily Heptagenioidea. Family Siphlonuridae. British representation. 3 species; S. alternatus, S.armatus and S. lacustris (the Duns and Spinners all colloquially called Summer Mayflies).
"""

# Initialize the OpenAI client with the API key
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# Messages to guide the generation of the character list
messages_character_list = [
    {"role": "system",
     "content": """
     You are a taxonomist specializing in morphological character analysis. 
     The following is a taxonomic description involving multiple species that share a phylogenetic relationship and belong to the same major group.
     Your task is to analyze the descriptions and extract morphological characteristics to generate a universal character list suitable for constructing a character matrix for phylogenetic analysis.
     """},
    {"role": "system",
     "content": """
     When generating the character list, please ensure the following:
     - **Taxonomic Standards**: The character list must conform to biological and taxonomic standards.
     - **Character Independence**: Each character should be independent, describing only one morphological attribute. Avoid combining multiple attributes into a single character.
     - **Character States**: For each character, list all possible states as observed in the descriptions. The states should be discrete and correspond to the relevant description content.
     - **Avoid Quantitative Characters**: Try to avoid selecting quantitative characters (e.g., measurements like length or size). Focus on qualitative characters that are more suitable for phylogenetic analysis.
     - **Shared Derived Characters**: Select characters that are informative for distinguishing among the species in the dataset, focusing on shared derived characters (synapomorphies).

     """},
    {"role": "system",
     "content": """
     Please present the character list in the following JSON format:
     ```json
     {
         "1": {
             "description": "Detailed description of Character 1",
             "states": {
                 "1": "Character 1, State 1",
                 "2": "Character 1, State 2"
             }
         },
         "2": {
             "description": "Detailed description of Character 2",
             "states": {
                 "1": "Character 2, State 1",
                 "2": "Character 2, State 2",
                 "3": "Character 2, State 3"
             }
         },
         ...
     }
     ```
     Ensure that the character numbers and state numbers are strings, and the entire output is a valid JSON object.

     """},
    {"role": "user",
     "content": f"""
     Please generate the character list as per the requirements above.
     Here is the combined taxonomic description of all species in the dataset:
     {The_original_description}

     """}
]



# Generate the initial character list using OpenAI API
response = client.chat.completions.create(
    model="gpt-4o-2024-08-06",
    messages=messages_character_list,
    stop=None,
    temperature=0.2,
    n=1
)

# Generate the character list
character_list = response.choices[0].message.content
print(character_list)

def API_matrix(description, character_list):
    """
    Generate taxonomic descriptions using OpenAI API based on the knowledge graph and character list.

    Args:
        knowledge_graph (dict): The knowledge graph of a species.
        character_list (str): The character list in string format.

    Returns:
        str: The generated taxonomic description.
    """
    messages_extract_information = [
        {"role": "system",
         "content": """
                 You are an expert in taxonomic information extraction, skilled in extracting morphological character information from standard taxonomic descriptions based on a given character list.
                 The character list specifies different characters and their states for all species in the dataset.
                 Please generate a list-form extraction result for each species, listing the state of each trait.
                 """},
        {"role": "system",
         "content": f"""
                 To extract character information, follow these steps:
                 1. **Strictly ensure that the final generated matrix contains exactly the characters listed in the character list, in the specified order. You must strictly adhere to this character list, neither adding nor omitting any traits.**
                 2. For each character, check if the species description includes any mention of the character's states. If it does, accurately record the corresponding state number.
                 3. If the description does not mention any character states, use your language reasoning skills to strictly check for words indicating the absence of the characteristic (e.g., "non", "no", "not"). If such terms are present, use the corresponding state number based on your reasoning.
                 4. If there is no mention of the character's states in the species description and your reasoning confirms the absence of relevant content, use "Gap" to represent this.
                 5. For trait states that do not exist (called "Missing"), use the symbol "-".

                 """},
        {"role": "system",
         "content": """
                After generating the extraction results in list format, please sort the traits and their corresponding states for each species **in the exact order they appear in the character list**, from left to right.
                In the example, the first '1' indicates that character 1 has state number 1 for the species.
                Arrange the list format results accurately as shown in the example.
                For content where a character may have multiple possible states, use (12) to indicate that the character has either state 1 or state 2.
                """},
        {"role": "system",
         "content": """
                 Please make the result follow these formats, and don't need to show any other things. Please only show the below results:
                 Matrix information:
                 Species A : 1 2 Gap 3 - (12) 2 (13)
                 """},
        {"role": "user",
         "content": f"""
             Here is the character list:

             {character_list}

             Here is the corresponding taxonomic description for:

             {description}
             """},

    ]

    response = client.chat.completions.create(
        model="gpt-4o-2024-08-06",
        messages=messages_extract_information,
        stop=None,
        max_tokens=1000,
        temperature=0,
        n=1
    )
    matrix_information = response.choices[0].message.content
    return matrix_information

# so here the main things need to split the whole description as each branch description to seprately generate the matrix
description1 = """
Ameletus Eaton
Imago. The compound eyes contiguous (in males), or widely separated (in females); rounded. Fore-wings with R5 and R4 joined basally. Hind-wings present. The hind-wings of the female imagines more than one fifth the length of the fore-wings. Hind tarsi slightly shorter than the tibia. Hind tarsi with 4 moveable segments. The hind tarsal claws unalike, being one pointed and one blunt. The abdomen with two tails. Male claspers separate. Nymph. The outer tails hairy on the inner side only. Gills mostly at the sides of the abdomen; not fringed with filaments on both sides. Classification. Superfamily Heptagenioidea. Family Siphlonuridae. British representation. 1 species (A. inopinatus).
"""
description2 = """
Baetis Leach
Imago. The compound eyes distinctly two-lobed (in males), or rounded (in females); upper lobe in the males, turbanate. Fore-wings with R5 detached basally from R4. The marginal fore-wing veinlets paired. Hind-wings present. The hind-wings of the female imagines no more than one fifth the length of the fore-wings. The hind-wing costa smoothly curved, or with a conspicuous projection. Hind tarsi with 4 moveable segments, or with 2–3 moveable segments (?). The abdomen with two tails. Nymph. The outer tails hairy on the inner side only. Gills mostly at the sides of the abdomen; not fringed with filaments on both sides; never comprising a plate bearing a tuft of filaments. Classification. Superfamily Baetoidea. Family Baetidae. British representation. 9 species; B. atrebatinus (Dark Olive Dun and Spinner), B. buceratus, B. digitatus, B. fuscatus (Pale Watery Dun and male Spinner, Golden Spinner female), B. muticus (Iron Blue Dun, Iron Blue or Jenny Spinner male, and Little Claret female Spinner), B. niger, B. rhodani (Large Dark Olive Dun and male Spinner, Large Red female Spinner), B. scambus Small Dark Olive Dun and male Spinner, (Small Red female Spinner), and B. vernus (Medium Olive Dun and male Spinner, Red Spinner female).
"""
description3 = """
Brachycercus Curtis
Eurycaenis Bengtsson. Imago. The compound eyes rounded. Second antennal segment three times as long as the first. Wings fringed in the imago. Fore-wings with R5 and R4 joined basally. Hind-wings absent. The fore-legs widely separated under the thorax. Hind tarsi with 4 moveable segments. The abdomen with three tails. Nymph. Gills mostly lying on the upper surface of the abdomen; not fringed with filaments on both sides. Classification. Superfamily Baetoidea. Family Caenidae. British representation. 1 species (B. harrisella).
"""
description4 = """
Caenis Stephens
Ordella Campion. Imago. The compound eyes rounded. Second antennal segment no more than twice as long as the first. Wings fringed in the imago. Fore-wings with R5 and R4 joined basally. Hind-wings absent. The fore-legs inserted relatively close together under the thorax. Hind tarsi with 4 moveable segments. The abdomen with three tails. Nymph. Gills mostly lying on the upper surface of the abdomen; not fringed with filaments on both sides. Classification. Superfamily Baetoidea. Family Caenidae. British representation. 5 species; C. horaria, C. luctuosa, C. macrura, C. rivulorum, C. robusta (all the Duns and Spinners colloquially named Angler’s Curse).
"""
description5 = """
Centroptilum Eaton
Imago. The compound eyes distinctly two-lobed (in males), or rounded (in females); upper lobe in the males, turbanate. Fore-wings with R5 detached basally from R4. The marginal fore-wing veinlets single. Hind-wings present. The hind-wings of the female imagines no more than one fifth the length of the fore-wings. The hind-wing costa with a conspicuous projection. Hind tarsi with 4 moveable segments, or with 2–3 moveable segments (?). The abdomen with two tails. Nymph. The outer tails hairy on the inner side only. Gills mostly at the sides of the abdomen; not fringed with filaments on both sides. Classification. Superfamily Baetoidea. Family Baetidae. British representation. 2 species; C. luteolum (Small Spurwing or Pale Watery Dun, Small Spurwing male Spinner, and Little Amber female Spinner), and C. pennulatum (Large Spurwing Dun and male Spinner, Large Amber female Spinner).
"""
description6 = """
Cloeon Leach
Imago. The compound eyes rounded. Fore-wings with R5 detached basally from R4. Hind-wings absent. The hind-wings of the female imagines more than one fifth the length of the fore-wings. Hind tarsi with 4 moveable segments. The first segment of the hind tarsus about twice as long as the second. The abdomen with two tails. Nymph. The outer tails hairy on the inner side only. Gills mostly at the sides of the abdomen; not fringed with filaments on both sides. Classification. Superfamily Baetoidea. Family Baetidae. British representation. 2 species; C. dipterum (Pond Olive or Lake Olive Dun, Pond Olive male Spinner, Apricot Spinner female), and C. simile.
"""
description7 = """
Ecdyonurus Eaton
Ecdyurus Eaton. Imago. The compound eyes contiguous (in males), or widely separated (in females); rounded. Wings more or less spotted with brown or blackish. Fore-wings with R5 and R4 joined basally. Hind-wings present. The hind-wings of the female imagines more than one fifth the length of the fore-wings. Hind tarsi with 5 moveable segments. The hind tarsal claws unalike, being one pointed and one blunt. The abdomen with two tails. Male claspers crossed. The lobes of the penis very broad-tipped, and closely approximated. Nymph. Gills mostly at the sides of the abdomen; not fringed with filaments on both sides; mostly consisting of a plate bearing a tuft of filaments. Classification. Superfamily Heptagenioidea. Family Heptageniidae. British representation. 4 species; E. dispar (Autumn or August Dun, Autumn or Red Spinners), E. insignis (Large Green Dun and Spinners), E. torrentis (Large Brook Dun and Spinners, or Great Red Spinner), and E. venosus (Late March Brown Dun and Spinners, or Great Red Spinner).
"""
description8 = """
Ephemera Linnaeus
Imago. The compound eyes rounded. Wings more or less spotted with brown or blackish. Fore-wings with veins M1 and Cu1 strongly strongly diverging basally; with R5 and R4 joined basally. Hind-wings present. The hind-wing costa smoothly curved. Hind tarsi with 4 moveable segments, or with 2–3 moveable segments. The abdomen with three tails. The lobes of the penis without recurved appendages. Nymph. Gills all densely fringed with filaments on both sides. Classification. Superfamily Ephemeroidea. Family Ephemeridae. British representation. 3 species; E. danica (Mayfly or Green Drake Dun, Mayfly male Spinner, and Mayfly, Spent Gnat or Black Drake female Spinner), E. lineata, and E. vulgata (Drake Mackerel Dun and Spinners).
"""
description9 = """
Ephemerella Walsh
Imago. The compound eyes rounded. Fore-wings with R5 and R4 joined basally. Hind-wings present. The hind-wing costa smoothly curved. Hind tarsi with 4 moveable segments. The abdomen with three tails. The lobes of the penis without recurved appendages. Nymph. Gills mostly lying on the upper surface of the abdomen; not fringed with filaments on both sides. Classification. Superfamily Baetoidea. Family Ephemerellidae. British representation. 2 species; E. ignita (Blue Winged Olive or B.W.O. Dun and male Spinner, Sherry Spinner female), and E. notata (Yellow Evening Dun and Spinners).
"""
description10 = """
Ephemerella Walsh
Imago. The compound eyes rounded. Fore-wings with R5 and R4 joined basally. Hind-wings present. The hind-wing costa smoothly curved. Hind tarsi with 4 moveable segments. The abdomen with three tails. The lobes of the penis without recurved appendages. Nymph. Gills mostly lying on the upper surface of the abdomen; not fringed with filaments on both sides. Classification. Superfamily Baetoidea. Family Ephemerellidae. British representation. 2 species; E. ignita (Blue Winged Olive or B.W.O. Dun and male Spinner, Sherry Spinner female), and E. notata (Yellow Evening Dun and Spinners).
"""

# Generate the matrix information, so we can directly build each extract matrix information
matrix1 = API_matrix(description1, character_list)
matrix2 = API_matrix(description2, character_list)
matrix3 = API_matrix(description3, character_list)
matrix4 = API_matrix(description4, character_list)
matrix5 = API_matrix(description5, character_list)
matrix6 = API_matrix(description6, character_list)
matrix7 = API_matrix(description7, character_list)
matrix8 = API_matrix(description8, character_list)
matrix9 = API_matrix(description9, character_list)
matrix10 = API_matrix(description10, character_list)
print(matrix4)


def convert_matrix_to_knowledge_graph(matrix_info):
    """
    Convert a species matrix into a knowledge graph format.

    Args:
        matrix_info (str): A string containing species name and character states, along with other potential noise.

    Returns:
        dict: A dictionary representing the knowledge graph of the species.
    """
    # 去除前面的描述信息，只保留矩阵部分
    if "Matrix information:" in matrix_info:
        matrix_info = matrix_info.split("Matrix information:")[1].strip()

    # 提取物种名称和矩阵
    parts = matrix_info.split(":")
    if len(parts) < 2:
        return {"error": "Invalid matrix format"}

    species_name = parts[0].strip()
    matrix = parts[1].strip().split()

    characteristics = {}

    for i, state in enumerate(matrix, start=1):
        if state == '-':
            characteristics[f"Character{i}"] = "Missing"
        elif state.startswith('(') and state.endswith(')'):
            states = state[1:-1].split()  # Split multiple states inside parentheses
            state_desc = " or ".join([f"state {s}" for s in states])
            characteristics[f"Character{i}"] = f"Multiple states: {state_desc}"
        else:
            characteristics[f"Character{i}"] = f"state {state}"

    return {species_name: {"Characteristics": characteristics}}


kg1 = convert_matrix_to_knowledge_graph(matrix1)
kg2 = convert_matrix_to_knowledge_graph(matrix2)
kg3 = convert_matrix_to_knowledge_graph(matrix3)
kg4 = convert_matrix_to_knowledge_graph(matrix4)
kg5 = convert_matrix_to_knowledge_graph(matrix5)
kg6 = convert_matrix_to_knowledge_graph(matrix6)
kg7 = convert_matrix_to_knowledge_graph(matrix7)
kg8 = convert_matrix_to_knowledge_graph(matrix8)
kg9 = convert_matrix_to_knowledge_graph(matrix9)
kg10 = convert_matrix_to_knowledge_graph(matrix10)
print(kg4)

def call_api_for_description(kg, character_list):
    """
    Generate taxonomic descriptions using OpenAI API based on the knowledge graph and character list.

    Args:
        knowledge_graph (dict): The knowledge graph of a species.
        character_list (str): The character list in string format.

    Returns:
        str: The generated taxonomic description.
    """
    messages = [
        {"role": "system", "content": """
            **You are a Taxonomic Assistant.**
            **Role and Expertise:**
            - You specialize in generating accurate and complete taxonomic descriptions by mapping feature state information to species morphology matrices.
            **Primary Objective:**
            - Utilize your natural language skills to generate accurate taxonomic descriptions for each species, **ensuring that all characters from the character list and morphological matrix are included without omission**.
            **Specific Requirements:**
            1. **Complete Inclusion of Characters**: Generate standard academic taxonomic descriptions that **include all characters** in the morphological matrix, accurately corresponding to the state of each character. **No characters should be omitted**.
            2. **Output Formats**: Generate descriptions in both **list form** and **paragraph form**.
               - In the **paragraph form**, indicate the **number of each character** as per the character list.
            """},
        {"role": "user", "content": """
            **Instructions:**
            1. **Strict Adherence to Data**: Generate taxonomic descriptions from the morphological matrix **without including any false or fabricated information**. **All characters must be included**.
            2. **Data Sources**:
               - **Morphological Matrix**: Provided in JSON format as a knowledge graph.
               - **Character Labels and State Labels**: Additional information containing detailed descriptions of each character and its corresponding states.
            3. **Handling Multiple States**:
               - Multiple states in the matrix (e.g., '1 or 2') indicate that the character of that taxon has **either state 1 or state 2**.
            4. **Consistency and Accuracy**:
               - Ensure that each character in the character list is addressed in the description, matching the corresponding state(s) from the matrix.
               - Do not omit or combine characters; treat each character independently.
            """},
        {"role": "assistant", "content": """
            Understood! I will:
            1. **Strictly follow the morphological matrix and character information** to generate accurate and complete taxonomic descriptions, ensuring **no characters are omitted**.
            2. **Provide the descriptions in both list form and paragraph form**, indicating the character numbers in the paragraph form.
            3. **Handle multiple states appropriately**, indicating when a character may have either of multiple states.
            4. **Avoid any false or fabricated content**, adhering strictly to the provided data.
            """},
        {"role": "user", "content": f"""
            **Additional Notes:**
            - Due to the large number of results, please show the taxonomic description of each taxon separately.
            - **Here is the morphological matrix for species {kg}:**
            - **Here is the character information {character_list}:**
            **Please proceed to generate the taxonomic descriptions as per the instructions above.**
            """},
        {"role": "assistant", "content": """
            Acknowledged. I will:
            - **Strictly ensure that the content of each taxonomic description is created in full accordance with the information in the knowledge graph and character list**, including **all characters without omission**.
            - **Provide the descriptions for each taxon separately**, in both list form and paragraph form, as specified.
            - **Avoid any false or fabricated content**.
            - **Don't miss any character**.
            """}
    ]

    response = client.chat.completions.create(
            model="gpt-4o-2024-08-06",
            messages=messages,
            stop=None,
            temperature=0,
            n=1
        )
    description_content = response.choices[0].message.content
    return description_content

#desc1 = call_api_for_description(kg1,character_list)
#desc2 = call_api_for_description(kg2,character_list)
#desc3 = call_api_for_description(kg3,character_list)
desc4 = call_api_for_description(kg4,character_list)
#desc5 = call_api_for_description(kg5,character_list)
#desc6 = call_api_for_description(kg6,character_list)
#desc7 = call_api_for_description(kg7,character_list)
#desc8 = call_api_for_description(kg8,character_list)
#desc9 = call_api_for_description(kg9,character_list)
#desc10 = call_api_for_description(kg10,character_list)
print(desc4)
def compare_description(description,desc,character_list):
    """
    Generate taxonomic descriptions using OpenAI API based on the knowledge graph and character list.

    Args:
        knowledge_graph (dict): The knowledge graph of a species.
        character_list (str): The character list in string format.

    Returns:
        str: The generated taxonomic description.
    """
    messages = [
        {"role": "system", "content": """
            You are a taxonomic expert specializing in comparing taxonomic descriptions to identify differences between them. 
            I will provide you with two taxonomic descriptions of the same species.

            Both descriptions will involve morphological characters from the provided character list. 
            Your task is to compare the two descriptions and identify any differences in the character states for each character mentioned in the list.
            **Please only display the characters where there is a difference between the two descriptions.**
            """},
        {"role": "user", "content": """
            Please display the differences in the following format:

            - **Character Name**:
              - Description 1: [state in description 1]
              - Description 2: [state in description 2]
            """},
        {"role": "user", "content": f"""
            Here is description 1: {description}, which is the original taxonomic description.
            Here is description 2: {desc}, another taxonomic description of the same species.

            I will also provide you with a character list relevant to both descriptions. 
            Your task is to compare the two descriptions and, according to the instructions above, identify any differences between the two descriptions regarding the characters in the provided character list.
            {character_list}
            Please follow the specified format to display the differences.
            """}
    ]
    response = client.chat.completions.create(
            model="gpt-4o-2024-08-06",
            messages=messages,
            stop=None,
            temperature=0,
            n=1
        )
    description_content = response.choices[0].message.content
    return description_content

compare2 = compare_description(description4,desc4,character_list)
print(compare2)