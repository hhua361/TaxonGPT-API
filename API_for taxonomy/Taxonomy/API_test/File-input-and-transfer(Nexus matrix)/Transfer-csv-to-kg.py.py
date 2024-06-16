import pandas as pd
import json

# Step 1: Read CSV File
def read_nexus_matrix(file_path):
    # Read the CSV file and return as a DataFrame
    df = pd.read_csv(file_path)
    return df

# Step 2: Build Knowledge Graph
def build_knowledge_graph(matrix):
    # Initialize an empty dictionary for the knowledge graph
    knowledge_graph = {}
    for _, row in matrix.iterrows():
        taxa = row.iloc[0]  # Access the species name using .iloc by position
        characteristics = {}
        for col in matrix.columns[1:]:  # Assume the first column is the species name
            state = row[col]
            if isinstance(state, str) and ',' in state:
                # Replace commas with 'and' in multi-state values
                state = state.replace(',', ' and ')
            characteristics[col] = str(state)  # Convert the state to string

        # Add the species and its characteristics to the knowledge graph
        knowledge_graph[taxa] = {
            'Characteristics': characteristics
        }
    return knowledge_graph

# Step 3: Save Knowledge Graph as JSON
def save_knowledge_graph_as_json(knowledge_graph, file_path):
    # Save the knowledge graph dictionary as a JSON file
    with open(file_path, 'w') as f:
        json.dump(knowledge_graph, f, indent=4)

# Example Usage
file_path = "D:/桌面/taxonomy_primary_result/The_GPT-4_result/Dataset_12 (Translating Niphargus barcodes from Switzerland into taxonomy with a description of two new species (Amphipoda, Niphargidae) ) 20/information gain methods/process_data.csv"
# Read the processed CSV file
nexus_matrix = read_nexus_matrix(file_path)
# Build the knowledge graph from the DataFrame
knowledge_graph = build_knowledge_graph(nexus_matrix)
save_file_path = "D:/桌面/taxonomy_primary_result/The_GPT-4_result/Dataset_12 (Translating Niphargus barcodes from Switzerland into taxonomy with a description of two new species (Amphipoda, Niphargidae) ) 20/information gain methods/matrix_knowledge_graph.json"
# Save the knowledge graph as a JSON file
save_knowledge_graph_as_json(knowledge_graph, save_file_path)
# Optional: Print the JSON structure for verification
knowledge_graph_json = json.dumps(knowledge_graph, indent=4)
print(knowledge_graph_json)
