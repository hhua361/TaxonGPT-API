def replace_indices_with_descriptions(differences, character_info):
    updated_differences = {}
    for feature_index, state_index in differences.items():
        feature_index = int(feature_index)
        state_index = str(state_index)
        if feature_index in character_info:
            description = character_info[feature_index]["description"]
            state_description = character_info[feature_index]["states"].get(state_index, "Unknown state")
            updated_differences[description] = state_description
    return updated_differences


def build_knowledge_graph(relationships, char_matrix, character_info):
    knowledge_graph = []

    def traverse_and_compare(parent, children):
        if len(children) == 2:
            node1, node2 = children
            differences1, differences2 = compare_features(char_matrix, node1, node2, character_info)
            differences1 = replace_indices_with_descriptions(differences1, character_info)
            differences2 = replace_indices_with_descriptions(differences2, character_info)
            knowledge_graph.append({
                'Parent': parent,
                'Node1': node1,
                'Differences1': differences1,
                'Node2': node2,
                'Differences2': differences2
            })
            if node1 in relationships:
                traverse_and_compare(node1, relationships[node1])
            if node2 in relationships:
                traverse_and_compare(node2, relationships[node2])

    for parent, children in relationships.items():
        traverse_and_compare(parent, children)

    return knowledge_graph
