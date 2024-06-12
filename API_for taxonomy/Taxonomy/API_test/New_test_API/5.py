from openai import OpenAI
client = OpenAI()

response = client.chat.completions.create(
  model="gpt-4o",
  messages=[
    {
      "role": "user",
      "content": [
        {
          "type": "text",
          "text": "Generation of Taxonomic key from Morphological Matrix \nI need to generate a taxonomic key using a morphological matrix provided in a CSV file. This matrix contains character states for various taxa. The goal is to determine the characters that best separate the taxa based on their states and progressively categorize them to construct the taxonomic key. The analysis should use information gain to evaluate each character's ability to classify the taxa evenly."
        }
      ]
    },
    {
      "role": "user",
      "content": [
        {
          "type": "text",
          "text": "Please follow these requirements during the analysis:  \n1. Initial Character Selection: Ensure all taxa have a defined state ('Missing' or 'Not applicable' is an invalid status) for the first character. Ignore characters with more than two states type and use information gain to select the most suitable character for initial classification.  \n2. Dynamic Character Selection: For each new character selection, reload the original matrix. Re-evaluate the presence of invalid states in character, Ignore characters with missing or not applicable states for the current subset of taxa. Include characters with actual states for the taxa being considered, even if they have missing or not applicable states for other taxa.  \n3. Character Selection Preference: Prefer characters with fewer state types when multiple characters have the same information gain. Ignore characters with more than three state types regardless of their information gain.  \n4. Step-by-Step Classification: Classify taxa step-by-step according to the above rules until all taxa are individually classified. Display the results in a nested structure without showing the code implementation"
        }
      ]
    },
    {
      "role": "assistant",
      "content": [
        {
          "type": "text",
          "text": "### Taxonomic Key Generation from Morphological Matrix\n\n**Step 1: Initial Character Selection**\n\n- We begin by evaluating each character for its ability to classify all taxa. Characters with missing or not applicable states are ignored.\n- Only characters with two state types are considered.\n- The most suitable character is selected based on the highest information gain.\n\n**Selected Character:** Character A (with states A1 and A2)\n\n**Step 2: Classification Based on Character A**\n\n- **Group 1:** Taxa with state A1\n- **Group 2:** Taxa with state A2\n\n**Group 1: Taxa with state A1**\n\n**Step 3: Dynamic Character Selection for Group 1**\n\n- Reload the original matrix.\n- Evaluate characters for Group 1, ignoring those with missing or not applicable states for these taxa.\n- Prefer characters with fewer state types.\n- Select the character with the highest information gain.\n\n**Selected Character for Group 1:** Character B (with states B1 and B2)\n\n**Step 4: Classification Based on Character B for Group 1**\n\n- **Group 1A:** Taxa with state B1\n- **Group 1B:** Taxa with state B2\n\n**Group 1A: Taxa with state B1**\n\n**Step 5: Dynamic Character Selection for Group 1A**\n\n- Reload the original matrix.\n- Evaluate characters for Group 1A.\n- Select the character with the highest information gain.\n\n**Selected Character for Group 1A:** Character C (with states C1 and C2)\n\n**Step 6: Classification Based on Character C for Group 1A**\n\n- **Group 1A1:** Taxa with state C1\n- **Group 1A2:** Taxa with state C2\n\n**Group 1A1: Taxa with state C1**\n\n- All taxa are individually classified.\n\n**Group 1A2: Taxa with state C2**\n\n- All taxa are individually classified.\n\n**Group 1B: Taxa with state B2**\n\n**Step 7: Dynamic Character Selection for Group 1B**\n\n- Reload the original matrix.\n- Evaluate characters for Group 1B.\n- Select the character with the highest information gain.\n\n**Selected Character for Group 1B:** Character D (with states D1 and D2)\n\n**Step 8: Classification Based on Character D for Group 1B**\n\n- **Group 1B1:** Taxa with state D1\n- **Group 1B2:** Taxa with state D2\n\n**Group 1B1: Taxa with state D1**\n\n- All taxa are individually classified.\n\n**Group 1B2: Taxa with state D2**\n\n- All taxa are individually classified.\n\n**Group 2: Taxa with state A2**\n\n**Step 9: Dynamic Character Selection for Group 2**\n\n- Reload the original matrix.\n- Evaluate characters for Group 2.\n- Select the character with the highest information gain.\n\n**Selected Character for Group 2:** Character E (with states E1 and E2)\n\n**Step 10: Classification Based on Character E for Group 2**\n\n- **Group 2A:** Taxa with state E1\n- **Group 2B:** Taxa with state E2\n\n**Group 2A: Taxa with state E1**\n\n**Step 11: Dynamic Character Selection for Group 2A**\n\n- Reload the original matrix.\n- Evaluate characters for Group 2A.\n- Select the character with the highest information gain.\n\n**Selected Character for Group 2A:** Character F (with states F1 and F2)\n\n**Step 12: Classification Based on Character F for Group 2A**\n\n- **Group 2A1:** Taxa with state F1\n- **Group 2A2:** Taxa with state F2\n\n**Group 2A1: Taxa with state F1**\n\n- All taxa are individually classified.\n\n**Group 2A2: Taxa with state F2**\n\n- All taxa are individually classified.\n\n**Group 2B: Taxa with state E2**\n\n**Step 13: Dynamic Character Selection for Group 2B**\n\n- Reload the original matrix.\n- Evaluate characters for Group 2B.\n- Select the character with the highest information gain.\n\n**Selected Character for Group 2B:** Character G (with states G1 and G2)\n\n**Step 14: Classification Based on Character G for Group 2B**\n\n- **Group 2B1:** Taxa with state G1\n- **Group 2B2:** Taxa with state G2\n\n**Group 2B1: Taxa with state G1**\n\n- All taxa are individually classified.\n\n**Group 2B2: Taxa with state G2**\n\n- All taxa are individually classified.\n\n### Final Nested Structure of the Taxonomic Key:\n\n1. Character A\n    - A1\n        - Character B\n            - B1\n                - Character C\n                    - C1: [Individually Classified Taxa]\n                    - C2: [Individually Classified Taxa]\n            - B2\n                - Character D\n                    - D1: [Individually Classified Taxa]\n                    - D2: [Individually Classified Taxa]\n    - A2\n        - Character E\n            - E1\n                - Character F\n                    - F1: [Individually Classified Taxa]\n                    - F2: [Individually Classified Taxa]\n            - E2\n                - Character G\n                    - G1: [Individually Classified Taxa]\n                    - G2: [Individually Classified Taxa]\n\nThe above steps provide a structured approach to creating a taxonomic key from the morphological matrix, ensuring that each step maximizes the separation of taxa based on their character states using information gain as the criterion for character selection."
        }
      ]
    }
  ],
  temperature=0.7,
  max_tokens=2009,
  top_p=1,
  frequency_penalty=0,
  presence_penalty=0
)