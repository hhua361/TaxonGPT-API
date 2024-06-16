import json
from openai import OpenAI
import os

# 设置OpenAI API密钥
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# 读取形态学矩阵数据
with open("D:/桌面/TEST-KG/nexus fix/matrix_knowledge_graph_22.json", "r", encoding="utf-8") as file:
    matrix_data = json.load(file)

# 读取特征信息数据
with open("D:/桌面/TEST-KG/nexus fix/updated_character_info.json", "r", encoding="utf-8") as file:
    character_info = json.load(file)

# 输出读取的数据以确认
print(matrix_data)
print(character_info)

def generate_taxonomic_key(matrix_data, character_info):
    messages = [
        {"role": "system",
         "content": "You are a taxonomy assistant skilled at calculating information gain and building taxonomic keys. Ensure accuracy and strict adherence to the provided guidelines. Prioritize characters based on information gain."},
        {"role": "user", "content":
            "Generation of Taxonomic Descriptions from Morphological Matrix" + \
            "Based on the provided morphological matrix (presented as a knowledge graph in JSON format), standard taxonomic descriptions are generated for all taxa in the matrix." + \
            "Additional CHARACTER labels and STATE labels will be provided, these labels contain a detailed description of each CHARACTER and its corresponding STATE." + \
            "Multiple states in the matrix (e.g., '1 and 2') indicate that the CHARACTER of that TAXA has both state 1 and state 2."
         },
        {"role": "assistant", "content":
            "Sure, I know how to generate a taxonomic description, and I will deal with the multiple states in the description."
         },
        {"role": "user", "content":
            "Specific requirements:" + \
            "1. Generate standard academic taxonomic descriptions, which need to include all characters in the morphological matrix and accurately correspond to the state of each character. " + \
            "2. Generate descriptions in list form and paragraph form. In paragraph form, the number of each character should be indicated."
         },
        {"role": "assistant", "content":
            "Sure, I will follow these specific requirements."
         },
        {"role": "user", "content":
            "Due to the large number of results, to avoid space constraints, please show the taxonomic description of each taxa separately." + \
            "Here is the JSON file: " + json.dumps(matrix_data) + "." + \
            "Here is the character info: " + json.dumps(character_info) + "."
         },
        {"role": "assistant", "content":
            "I will step by step show the results."
         }
    ]

    response = OpenAI.chat.completions.create(
        model="gpt-4o",
        messages=messages,
        stop=None,
        temperature=0,
        stream=True,
        n=1
    )

    result = ""
    for chunk in response:
        if chunk.choices[0].delta.get("content"):
            result += chunk.choices[0].delta.content
            print(chunk.choices[0].delta.content, end="")

    return result

nexus_content = generate_taxonomic_key(matrix_data, character_info)
print(nexus_content)
