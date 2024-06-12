import tiktoken

def count_tokens(text, model="gpt-4"):
    encoding = tiktoken.encoding_for_model(model)
    tokens = encoding.encode(text)
    return len(tokens)

def count_message_tokens(messages, model="gpt-4"):
    total_tokens = 0
    for message in messages:
        role_tokens = count_tokens(message['role'], model)
        content_tokens = count_tokens(message['content'], model)
        total_tokens += role_tokens + content_tokens
    return total_tokens

messages = [
    {
        "role": "system",
        "content": """# Initial Character Classify Result #
- **State 1**:
  - Equisetum_arvense
  - Equisetum_telmateia

- **State 2**:
  - Equisetum_pratense
  - Equisetum_sylvaticum

- **State 3**:
  - Equisetum_fluviatile
  - Equisetum_hyemale
  - Equisetum_litorale
  - Equisetum_moorei
  - Equisetum_palustre
  - Equisetum_ramosissimum
  - Equisetum_trachyodon
  - Equisetum_variegatum"""
    }
]

total_tokens = count_message_tokens(messages)
print(f"Total tokens: {total_tokens}")
