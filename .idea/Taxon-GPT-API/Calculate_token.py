import tiktoken


def count_tokens(text, model="gpt-4"):
    """
    Count the number of tokens in the given text based on the encoding for the specified model.

    Args:
        text (str): The input text to be tokenized.
        model (str): The model used for encoding (default: "gpt-4").

    Returns:
        int: The number of tokens in the text.
    """
    encoding = tiktoken.encoding_for_model(model)
    tokens = encoding.encode(text)
    return len(tokens)


def count_message_tokens(messages, model="gpt-4"):
    """
    Count the total number of tokens in a list of messages. Each message is expected to have a 'role' and 'content' field.

    Args:
        messages (list): A list of dictionaries, where each dictionary contains a 'role' and 'content'.
        model (str): The model used for encoding (default: "gpt-4").

    Returns:
        int: The total number of tokens for all messages.
    """
    total_tokens = 0
    for message in messages:
        role_tokens = count_tokens(message['role'], model)
        content_tokens = count_tokens(message['content'], model)
        total_tokens += role_tokens + content_tokens
    return total_tokens


# Academic Example: Taxonomic description in a concise format.
messages = [
    {
        "role": "system",
        "content": """### Taxonomic Description for *Huperzia selago*

        #### Features (List Format):
        1. **Leaves**: Spiral arrangement; stiff and linear-lanceolate.
        2. **Strobili**: Absent; instead, spores are produced in axillary sporangia.
        3. **Spores**: Produced in axils of specialized leaves, green when mature.
        4. **Rhizome**: Creeping and short, often buried in moss.
        5. **Habitat**: Commonly found in alpine regions and boreal forests.
        6. **Growth Form**: Evergreen perennial with no visible differentiation between fertile and sterile shoots.

        #### Paragraph Form:
        *Huperzia selago* is a small, creeping, evergreen lycophyte characterized by spiral leaf arrangement with stiff, linear-lanceolate leaves. Unlike many related species, it lacks strobili, producing spores in the axils of specialized leaves. The rhizome is short and buried, aiding in its alpine and boreal habitat preferences. This species thrives in mossy and moist environments, typically forming dense mats."""
    }
]

# Count the total tokens in the academic example
total_tokens = count_message_tokens(messages)
print(f"Total tokens: {total_tokens}")
