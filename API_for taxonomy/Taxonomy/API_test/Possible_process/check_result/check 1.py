import re
initial_response = """
{
    "Character": "Character1",
    "States": {
        "1": ["Diphasiastrum_alpinum", "Diphasiastrum_complanatum", "Huperzia_selago", "Lycopodiella_inundata", "Lycopodium_annotinum", "Lycopodium_clavatum", "Selaginella_kraussiana", "Selaginella_selaginoides"],
        "2": ["Isoetes_echinospora", "Isoetes_histrix", "Isoetes_lacustris"]
    }
}
"""

def parse_classification_result(result_text):
        classification = {"Character": None, "States": {}}
        try:
            # 尝试匹配Character
            character_match = re.search(r'"Character": "([^"]+)"', result_text)
            if character_match:
                classification["Character"] = character_match.group(1)
            else:
                raise ValueError("Character not found in the result text.")

            # 尝试匹配各个State和对应的species
            state_sections = re.findall(r'"(\d+|[^"]+)":\s*\[(.*?)\]', result_text)
            if not state_sections:
                raise ValueError("No states found in the result text.")

            for state, species_block in state_sections:
                species_list = re.findall(r'"([^"]+)"', species_block)
                if not species_list:
                    raise ValueError(f"No species found for state {state}.")
                classification["States"][state] = species_list

        except Exception as e:
            print(f"Error parsing classification result: {e}")
            # 可以根据需求决定在遇到错误时是否返回空的分类结果或抛出异常
            raise e  # 或者 return classification

        return classification

parsed_initial_classification = parse_classification_result(initial_response)
print(initial_response)


def recursive_classification(groups, final_classification, classification_results, depth=0, max_depth=10):
    """
    Recursive classification function to process groups and store results.

    :param groups: Groups to be processed
    :param final_classification: Final classification result
    :param classification_results: Classification results
    :param depth: Current recursion depth
    :param max_depth: Maximum recursion depth
    :return: Final classification result
    """
    # Continue looping while the groups list is not empty
    while groups:
        try:
            # Pop the first group from the list, getting the state and current group of species
            state, current_group = groups.pop(0)
            print(f"Processing group with state: {state}, species: {current_group}, at depth: {depth}")

            # If the current group has only one species, add it to the final classification
            if len(current_group) == 1:
                final_classification[current_group[0]] = current_group
            # If the current recursion depth has reached the maximum depth, stop further classification
            elif depth >= max_depth:
                print(f"Reached max depth {max_depth}. Stopping further classification for group: {current_group}")
                final_classification[state] = current_group
            else:
                # Call the classify_group function to classify the current group
                classification_result = classify_group(current_group)
                # Store the classification result in classification_results
                classification_results[state] = classification_result

                # Parse the classification result, create new subgroups, and add them to groups for further classification
                new_groups = []
                parsed_result = parse_classification_result(classification_result)
                for new_state, new_species_list in parsed_result["States"].items():
                    new_groups.append((new_state, new_species_list))

                # Recursively call itself to process new subgroups, increasing the recursion depth
                recursive_classification(new_groups, final_classification, classification_results, depth + 1, max_depth)

        except Exception as e:
            # Catch exceptions and print error messages
            print(f"Error processing group with state: {state}, species: {current_group}, at depth: {depth}")
            print(f"Exception: {e}")
            raise e

    return final_classification


# Assume the variables have been initialized
# Dictionary to store the final classification result
final_classification = {}

# Dictionary to store the API classification results for each state
classification_results = {}

# Example initial groups
groups = [
    ("1", ["species1", "species2"]),
    ("2", ["species3", "species4", "species5"])
]

# Set the maximum recursion depth, adjust based on specific needs
max_depth = 5  # Can be adjusted based on the hierarchical structure of input data and application requirements

# Call the recursive classification function to process groups and store results
final_classification = recursive_classification(groups, final_classification, classification_results, depth=0, max_depth=max_depth)

# Print the final classification results
print("Final Classification:")
print(json.dumps(final_classification, indent=2, ensure_ascii=False))

# Print the classification results from the API calls
print("\nClassification Results:")
print(json.dumps(classification_results, indent=2, ensure_ascii=False))

