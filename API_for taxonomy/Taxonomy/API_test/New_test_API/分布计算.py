from openai import OpenAI
import os
import json

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

with open("D:/桌面/normalized_matrix_knowledge_graph_22.json", "r") as file:
    matrix_data = json.load(file)
with open("D:/桌面/TEST-KG/nexus fix/updated_character_info.json", "r", encoding="utf-8") as file:
    character_info = json.load(file)
def generate_taxonomic_key(matrix_data, character_info):
    matrix_data_str = json.dumps(matrix_data)
    character_info_str = json.dumps(character_info)
    messages = [
        {"role": "system",
         "content": "You are a taxonomy assistant skilled at generate the standard description. Ensure accuracy and strict adherence to the provided guidelines. "},
        {"role": "user", "content":
            "Generation of Taxonomic Descriptions from Morphological Matrix" + \
            "Based on the provided morphological matrix (presented as a knowledge graph in JSON format), standard taxonomic descriptions are generated for all taxa in the matrix." + \
            "Additional CHARACTER labels and STATE labels will be provided, these labels contain a detailed description of each CHARACTER and its corresponding STATE." + \
            "Multiple states in the matrix (e.g., '1 and 2') indicate that the CHARACTER of that TAXA has both state 1 and state 2."
         },
        {"role": "assistant", "content":
            "Sure, I understand, I will based on the morphological matrix and character information the to generate the taxonomic description, i will also careful to deal with the multiple states in the description."
         },
        {"role": "user", "content":
            "Specific requirements:" + \
            "1. Generate standard academic taxonomic descriptions, which need to include all characters in the morphological matrix and accurately correspond to the state of each character. " + \
            "2. Generate descriptions in list form and paragraph form. In paragraph form, the number of each character should be indicated."
         },
        {"role": "assistant", "content":
            "Sure, I will follow these specific requirements,first strict to based on the morphological matrix and character information to generate taxonomic description, to make sure the result is correct" + \
            "Secondly, I will generate separate taxonomic descriptions in list and paragraph form with corresponding ordinal numbers. "
         },
        {"role": "user", "content":
            "Due to the large number of results, to avoid space constraints, please show the taxonomic description of each taxa separately." + \
            "Here is the JSON file: " + matrix_data_str + "." 
            "Here is the character info: " + character_info_str + "."
         },
        {"role": "assistant", "content":
            "I will follow the steps above to generate taxonomic descriptions for each taxa one by one and strictly adhering to what is in the morphological matrix and CHARACTER information"
         }
    ]
# [{"type":"text","text":}]
    response =  client.chat.completions.create(
        model="gpt-4o",
        messages=messages,
        stop=None,
        temperature=0,
        stream =True,
        n = 1
    )


    for chunk in response:
        if chunk.choices[0].delta.content is not None:
            print(chunk.choices[0].delta.content, end="")

    return chunk.choices[0].delta.content
# 可能有用需要尝试的东西：
  #  messages.append({"role": "assistant", "content": response.choices[0].message.content)
  #  prompt = “”
  #  messages.append({"role": "assistant", "content":prompt})
  #通过这种方法来生成一步一步的结果，例如第一步计算出first character 以及对应的subgroup，然后再次调回只对某个subgroup来进行计算
  # 我感觉我对于API的使用还有很多东西需要学习
nexus_content = generate_taxonomic_key(matrix_data, character_info)
print(nexus_content)


