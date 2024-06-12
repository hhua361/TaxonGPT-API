import re
import json
import re

def parse_charlabels(charlabels_content):
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
        state_dict = {i + 1: state for i, state in enumerate(states)}
        character_info[char_index] = {
            "description": description,
            "states": state_dict
        }
    return character_info

# 示例CHARLABELS内容
charlabels_content = """
[1(1)] 'body size'
[2(3)] 'telson with'
[3(4)] 'telson with'
[4(5)] 'telson spines <lenght>'
[5(6)] 'epimeral plate III'
[6(7)] 'urosoma segment I'
[7(8)] 'inner lobe of maxilla I'
[8(9)] 'outer lobe of maxilla I'
[9(10)] 'propodus and carpus of gnathop'
[10(11)] 'propodus of gnathopod II <size'
[11(12)] 'gnathopod dactylus with'
[12(13)] 'dactylus of pereopod III-VII'
[13(14)] 'coxal plate IV'
[14(15)] 'dactyli III-IV'
[15(16)] 'uropod I <distal setae>'
[16(17)] 'uropod I <ratio of uropod rami'
[17(18)] 'uropod I <sexual dimorphism>'
[18(19)] 'uropod III'
;
"""

# 示例STATELABELS内容
statelabels_content = """
1 'up to 10 mm' 'more than 10 mm',
2 'apical, lateral and dorsal spi' 'apical and lateral spines'
     'apical spines alone' 'apical and dorsal spines',
3 '3, rarely 4 apical spines per' '5 or more apical spines per lo',
4 'long, longer than 1/2 of the t' 'short-to mid sized, at most 0.',
5 'subrounded, posterior and vent' 'angular, ventral margin slight',
6 'single seta or spine dorso-pos' 'two or more setae and/or spine',
7 'one to two setae' 'three or more setae',
8 'with 7 spines, typically inner' 'with 7 spines, inner four with'
     'with 7 spines, all with severa' 'more than 7 spines, all fine p',
9 'carpus longer than propodus, p' 'carpus as long as propodus or'
     'carpus as long as propodus or',
10 'much larger than propodus of g' 'slightly larger than propodus',
11 'single seta at outer margin' 'more than one seta on outer ma',
12 'at most one spine at the base' 'at least one additional spine',
13 'much deeper than broad, proxim' 'more broad than deep, or as br',
14 'long and slender, longer than' 'slender or stout, at most 1/2',
15 'distal setae on rami not remak' 'long setae distally on rami (b',
16 'inner ramus slightly to remark' 'inner ramus shorter than outer',
17 'sexually dimorphic: inner ramu' 'sexually non-dimorphic: the ra'
     'sexual dimorphism not know',
18 'sexually dimorphic: distal art' 'sexually non-dimorphic: distal'
     'sexual dimorphism not known',
"""

# 解析CHARLABELS部分
charlabels = parse_charlabels(charlabels_content)

# 解析STATELABELS部分
statelabels = parse_statelabels(statelabels_content)

# 结合解析结果生成character_info字典
character_info = combine_labels_and_states(charlabels, statelabels)

# 打印结果
print(json.dumps(character_info, indent=4))
output_path = "D:/桌面/taxonomy_primary_result/The_GPT-4_result/Dataset_12 (Translating Niphargus barcodes from Switzerland into taxonomy with a description of two new species (Amphipoda, Niphargidae) ) 20/character_info.json"
with open(output_path, "w") as f:
    json.dump(character_info, f, indent=4)


