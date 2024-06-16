import pandas as pd

def preprocess_data(file_path, output_path):
    data = []
    headers = ['taxa']
    with open(file_path, 'r') as file:
        matrix_start = False  # Flag to indicate if matrix data reading has started
        for line in file:
            if line.strip() == 'MATRIX':
                matrix_start = True
                continue
            if matrix_start:
                if line.strip() == ';':  # End of matrix data
                    break
                if not line.strip():  # Skip empty lines
                    continue
                parts = line.strip().split()
                if len(parts) == 0:  # Skip lines that result in empty parts
                    continue
                species = parts[0]  # Extract species name
                traits = ''.join(parts[1:])  # Concatenate trait data into a single string
                # Parse trait data
                i = 0
                species_traits = []
                trait_count = 1
                while i < len(traits):
                    if traits[i] == '(':
                        # Handle compound states within parentheses, separated by commas
                        i += 1
                        state = ''
                        while traits[i] != ')':
                            if traits[i].isdigit():
                                state += 'state ' + traits[i] + ', '
                            i += 1
                        species_traits.append(state.rstrip(', '))  # Remove trailing comma and space
                    elif traits[i] == '?':
                        # Handle missing data
                        species_traits.append('Missing')
                    elif traits[i] == '-':
                        # Handle not applicable data
                        species_traits.append('Not Applicable')
                    else:
                        # Handle ordinary single states
                        species_traits.append('state ' + traits[i])
                    i += 1
                    if len(headers) <= trait_count:
                        headers.append(f'Character{trait_count}')
                    trait_count += 1
                data.append([species] + species_traits)
    # Convert to DataFrame
    df = pd.DataFrame(data, columns=headers)
    # Save as CSV to the specified path
    df.to_csv(output_path, index=False)

# Input file path
file_path = "D:/桌面/taxonomy_primary_result/The_GPT-4_result/Dataset_6 (The families of gymnosperms) 10/Information gain methods/nexdata"
# Output file save path
output_path = "D:/桌面/ancestral_states_1.csv"

# Process the file and save
preprocess_data(file_path, output_path)
