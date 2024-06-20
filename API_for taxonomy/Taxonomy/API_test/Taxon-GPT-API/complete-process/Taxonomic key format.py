# type 1
classification_data = {
    "Character 1: The rhizomes <whether tuberous>": {
        "State 1: Bearing tubers": {
            "Character 10: The longitudinal internodal grooves <in the main stem internodes of the assimilating shoots, details>": {
                "State 1: Fine, the ribs between them not prominent": "Equisetum litorale",
                "State 2: Deep, with prominent ridges between": "Equisetum palustre"
            }
        },
        "State 1 and 2: Bearing tubers;;Not tuberous": {
            "Character 2: The shoots <dimorphism>": {
                "State 1: Conspicuously dimorphic: the cone-bearing stems thick, unbranched, brown and non-assimilating, appearing in early spring and withering before the emergence of the sterile, branched, green, persistent ones": {
                    "Character 10: The longitudinal internodal grooves <in the main stem internodes of the assimilating shoots, details>": {
                        "State 1: Fine, the ribs between them not prominent": "Equisetum telmateia",
                        "State 2: Deep, with prominent ridges between": "Equisetum arvense"
                    }
                },
                "State 2: Distinguishable as fertile and sterile: both types produced at the same time, but those bearing cones remaining non-green and unbranched until after spore dispersal, and only later becoming green and branching so as to resemble the sterile stems vegetatively": "Equisetum sylvaticum",
                "State 3: All green and alike vegetatively, the sterile and cone-bearing shoots emerging at the same time": "Equisetum fluviatile"
            }
        },
        "State 2: Not tuberous": {
            "Character 8: The main stems <of the assimilating shoots, persistence>": {
                "State 1: Persisting through the winter": {
                    "Character 7: The main stems <of the assimilating shoots, branching>": {
                        "State 1: Bearing whorls of slender branches at the nodes": "Equisetum ramosissimum",
                        "State 2 and 3: Sparingly branched, the branches solitary and similar to the main stem;;Simple": {
                            "Character 6: The main stems <of the assimilating shoots, rough or smooth>": {
                                "State 1: Very rough": "Equisetum trachyodon",
                                "State 2: Slightly rough": "Equisetum variegatum"
                            }
                        },
                        "State 3: Simple": "Equisetum hyemale"
                    }
                },
                "State 2: Dying down in autumn": {
                    "Character 2: The shoots <dimorphism>": {
                        "State 2: Distinguishable as fertile and sterile: both types produced at the same time, but those bearing cones remaining non-green and unbranched until after spore dispersal, and only later becoming green and branching so as to resemble the sterile stems vegetatively": "Equisetum pratense",
                        "State 3: All green and alike vegetatively, the sterile and cone-bearing shoots emerging at the same time": "Equisetum moorei"
                    }
                }
            }
        }
    }
}

# Initialize step counter
step_counter = 1
steps = []

# Recursive function to generate classification key
def generate_classification_key(data, current_step, parent_step=None):
    global step_counter
    if isinstance(data, dict):
        state_steps = []
        step_map = {}
        for character, states in data.items():
            for state, next_level in states.items():
                full_state_description = f"{character.split(': ')[1]}：{state.split(': ')[1]}"  # Combine character and state descriptions
                if isinstance(next_level, dict):
                    step_counter += 1
                    next_step_prefix = str(step_counter)
                    state_steps.append(f"    - {full_state_description} ........ {next_step_prefix}")  # Use combined description
                    step_map[step_counter] = (next_level, current_step)
                else:
                    state_steps.append(f"    - {full_state_description} ........ {next_level}")  # Use combined description
        if parent_step:
            steps.append(f"{current_step}({parent_step}).")
        else:
            steps.append(f"{current_step}.")
        steps.extend(state_steps)
        for step, (next_level, parent_step) in step_map.items():
            generate_classification_key(next_level, step, parent_step)
    else:
        # If data is not a dictionary, do not recurse
        return

# Generate classification key
generate_classification_key(classification_data, 1)

# Format output
classification_key = "\n".join(steps)
print(classification_key)

# Write results to file
with open("classification_key.txt", "w") as f:
    f.write(classification_key)





# type 2
# Initialize step counter
step_counter = 1
steps = []
outer_steps = []


# Recursive function to generate classification key
def generate_classification_key(data, current_step, parent_step=None, outer_step=False):
    global step_counter
    if isinstance(data, dict):
        for character, states in data.items():
            # Ensure step_prefix is correct
            if parent_step is None:
                step_prefix = str(current_step)
            else:
                step_prefix = f"{current_step}({parent_step})"

            step_description = f"{step_prefix}. {character.split(': ')[1]}"  # Only use description
            if outer_step:
                outer_steps.append(step_description)  # Record outermost steps
            else:
                steps.append(step_description)  # Record current step
            state_steps = []
            step_map = {}
            for state, next_level in states.items():
                if isinstance(next_level, dict):
                    step_counter += 1
                    next_step_prefix = str(step_counter) if parent_step is None else f"{step_counter}"
                    state_steps.append(f"    - {state.split(': ')[1]} ........ {next_step_prefix}")  # Only use description
                    step_map[step_counter] = (next_level, current_step)
                else:
                    state_steps.append(f"    - {state.split(': ')[1]} ........ {next_level}")  # Only use description
            steps.extend(state_steps)
            for step, (next_level, current_step) in step_map.items():
                generate_classification_key(next_level, step, current_step)
            current_step += 1  # Ensure the outermost steps are in order
    else:
        # If data is not a dictionary, do not recurse
        return


# Generate classification key
generate_classification_key(updated_classification_key, 1, outer_step=True)

# Sort the outermost steps
sorted_outer_steps = sorted(outer_steps, key=lambda x: int(x.split('.')[0]))

# Combine sorted outermost steps with other steps
sorted_steps = sorted_outer_steps + [step for step in steps if not any(step.startswith(f"{i}.") for i in range(1, len(outer_steps) + 1))]

# Format output
classification_key = "\n".join(sorted_steps)
print(classification_key)

# Write results to file
with open("classification_key.txt", "w") as f:
    f.write(classification_key)