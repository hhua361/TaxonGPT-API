import re
import json

def parse_charlabels(charlabels_content):
    """
    Character information template
    CHARLABELS
    [1(4)] 'The rhizomes <whether tuberous>'
    [2(5)] 'The shoots <dimorphism>'
    [3(8)] 'The brown, non-assimilating fertile stems <number of sheaths>'
    [4(12)] 'The main stems <of the assimilating shoots, carriage>'
    [5(13)] 'The main stems <of the assimilating shoots, colour>'
    [6(14)] 'The main stems <of the assimilating shoots, rough or smooth>'
    [7(15)] 'The main stems <of the assimilating shoots, branching>'
    [8(16)] 'The main stems <of the assimilating shoots, persistence>'
    [9(17)] 'The main stem internodes <of the assimilating shoots, whether swollen>'
    [10(19)] 'The longitudinal internodal grooves <in the main stem internodes of the assimilating shoots, details>'
    [11(20)] 'The main stem internodes <of the assimilating shoots, presence of a central hollow>'
    [12(21)] 'Central hollow <of the main stem internodes of assimilating shoots, relative diameter>'
    [13(22)] 'Endodermis <in main stem internodes of assimilating shoots, location>'
    [14(24)] 'The main stem sheaths <of assimilating shoots, length relative to breadth>'
    [15(25)] 'The main stem sheaths <of assimilating shoots, loose or appressed>'
    [16(27)] 'The teeth <of the main stem sheaths of assimilating shoots, ribbing>'
    [17(29)] 'The teeth <of the main stem sheaths of assimilating shoots, persistence>'
    [18(30)] 'The primary branching <regularity>'
    [19(31)] 'The primary branches <when present, few or many>'
    [20(32)] 'The primary branches <carriage>'
    [21(33)] 'The primary branches <of assimilating shoots, whether themselves branched>'
    [22(37)] 'The first <primary> branch internodes <of assimilating shoots, relative length>'
    [23(38)] 'The primary branch internodes'
    [24(39)] 'Stomata <of assimilating shoots, insertion relative to the adjacent epidermal cells>'
    [25(41)] 'The cones <blunt or apiculate>'
    [26(42)] 'Spores <whether fertile>'
    [27(43)] 'Spores released <months released>'
    [28(46)] 'Subgenus'
    [29(47)] 'Section <of subgenus Equisetum>'
    ;
    """
    charlabels = {}
    lines = charlabels_content.strip().split("\n")
    char_pattern = re.compile(r"\[(\d+)\(\d+\)\]\s+'(.+?)'")
    for line in lines:
        match = char_pattern.match(line.strip().rstrip(','))
        if match:
            char_index = int(match.group(1))
            description = match.group(2)
            charlabels[char_index] = description
    return charlabels


def parse_statelabels(statelabels_content):
    """
    State information template
    STATELABELS
    1 'Bearing tubers' 'Not tuberous',
    2 'Conspicuously dimorphic: the cone-bearing stems thick, unbranched, brown and non-assimilating, appearing in early spring and withering before the emergence of the sterile, branched, green, persistent ones' 'Distinguishable as fertile and sterile: both types produced at the same time, but those bearing cones remaining non-green and unbranched until after spore dispersal, and only later becoming green and branching so as to resemble the sterile stems vegetatively'
         'All green and alike vegetatively, the sterile and cone-bearing shoots emerging at the same time',
    3 'With numerous sheaths and relatively short internodes' 'With only 4 to 6 relatively distant sheaths',
    4 'Erect' 'Decumbent',
    5 'Bright green' 'Dull green',
    6 'Very rough' 'Slightly rough' 'Smooth',
    7 'Bearing whorls of slender branches at the nodes' 'Sparingly branched, the branches solitary and similar to the main stem' 'Simple',
    8 'Persisting through the winter' 'Dying down in autumn',
    9 'Somewhat swollen' 'Not swollen',
    10 'Fine, the ribs between them not prominent' 'Deep, with prominent ridges between',
    11 'Solid' 'With a central hollow',
    12 'Much less than half the diameter of the internode' 'About half the diameter of the internode'
         'More than half the diameter of the internode',
    13 'Surrounding the individual vascular bundles' 'Comprising a single layer outside the ring of vascular bundles'
         'Comprising two layers, one outside and the other inside the ring of vascular bundles',
    14 'About as broad as long' 'Longer than broad',
    15 'Loose' 'Appressed',
    16 'Ribbed' 'Not ribbed',
    17 'Persistent' 'Caducous',
    18 'Symmetrical' 'Asymmetrical',
    19 'Few' 'Numerous',
    20 'Ascending' 'Spreading' 'Drooping',
    21 'Simple' 'Secondarily branched',
    22 'Much shorter than the subtending sheaths' 'At least as long as the subtending sheaths, at least on the upper parts of the stem',
    23 'Solid' 'Hollow',
    24 'Sunken' 'Not sunken',
    25 'Blunt' 'Apiculate',
    26 'Fertile' 'Abortive',
    27 'April' 'May' 'June' 'July' 'August' 'September',
    28 'Equisetum' 'Hippochaete',
    29 'Aestivalia' 'Subvernalia' 'Vernalia',
    ;
    """
    statelabels = {}
    lines = statelabels_content.strip().split("\n")
    current_char = None
    states = []

    for line in lines:
        if re.match(r'^\d+', line):
            if current_char is not None:
                statelabels[current_char] = states
            parts = line.split(' ', 1)
            current_char = int(parts[0])
            states = parts[1].strip().strip(',').split("' '")
            states = [state.strip("'") for state in states]
        else:
            additional_states = line.strip().strip(',').split("' '")
            additional_states = [state.strip("'") for state in additional_states]
            states.extend(additional_states)

    if current_char is not None:
        statelabels[current_char] = states

    return statelabels


def combine_labels_and_states(charlabels, statelabels):
    character_info = {}
    for char_index, description in charlabels.items():
        states = statelabels.get(char_index, [])
        state_dict = {str(i + 1): state for i, state in enumerate(states)}
        character_info[str(char_index)] = {
            "description": description,
            "states": state_dict
        }
    return character_info


def extract_nexus_sections(nexus_content):
    charlabels_content = ""
    statelabels_content = ""
    lines = nexus_content.strip().split("\n")
    in_charlabels = False
    in_statelabels = False

    for line in lines:
        if "CHARLABELS" in line:
            in_charlabels = True
            continue
        if "STATELABELS" in line:
            in_statelabels = True
            continue
        if ";" in line:
            in_charlabels = False
            in_statelabels = False

        if in_charlabels:
            charlabels_content += line + "\n"
        if in_statelabels:
            statelabels_content += line + "\n"

    return charlabels_content, statelabels_content


def parse_nexus_file(file_path):
    with open(file_path, 'r') as file:
        nexus_content = file.read()

    charlabels_content, statelabels_content = extract_nexus_sections(nexus_content)
    charlabels = parse_charlabels(charlabels_content)
    statelabels = parse_statelabels(statelabels_content)
    character_info = combine_labels_and_states(charlabels, statelabels)

    return character_info


file_path = "D:/桌面/taxonomy_primary_result/The_GPT-4_result/Dataset_3 (The Lycopodiales (Diphasiastrum, Huperzia, Isoetes, Lycopodium, Selaginella)) 4/Information gain methods/nexdata"
character_info = parse_nexus_file(file_path)
print(json.dumps(character_info, indent=4))

