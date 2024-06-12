from openai import OpenAI
client = OpenAI()

completion = client.chat.completions.create(
  model="gpt-3.5-turbo",
  messages=[
    {"role": "system",
     "content": "You are a helpful assistant, skilled in creating NEXUS file formats for phylogenetic analysis."},
    {"role": "user", "content": "I need to convert a taxonomy description into a NEXUS file. Can you help?"},
    {"role": "assistant", "content": "Sure, I can help with that. Please provide the taxonomy description."},
    {"role": "user", "content": "Start with the #NEXUS header."},
    {"role": "user","content": "Follow the NEXUS standards to include the BEGIN DATA block, specifying DIMENSIONS and FORMAT."},
    {"role": "user","content": "Create the MATRIX section, listing each species along with their morphological traits."},
    {"role": "user","content": "Ensure the output adheres closely to the structure and requirements of the NEXUS format, especially in the MATRIX section."},
    {"role": "user", "content": "Close the NEXUS file with the 'END;' statement."},
  ]
)

print(completion.choices[0].message)
