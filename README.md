TaxonGPT: Efficient Taxonomic Data Conversion and Key Generation with GPT-4o model
====

## Installation
To use the TaxonGPT function, you can download the TaxonGPT.py file located in the main directory. Then, run it in your local Python environment.
> ### Steps:
1. To use the TaxonGPT function, you can download the TaxonGPT.py file located in the main directory. Then, run it in your local Python environment.
2. Ensure you have Python installed on your system.
3. Run the following command in your terminal to execute the file:
```python
python path/to/TaxonGPT.py
```

## Overview
![README](https://github.com/user-attachments/assets/4b1afa2e-4398-4a0f-9654-7fb72f73bebf)

> ### Input file
TaxonGPT is dedicated to converting information from Nexus matrices into biologically meaningful taxonomic information and accurate natural language descriptions of species. To achieve comprehensive taxonomic data, the input files for TaxonGPT include:
* **Nexus Matrix** (nexus_file_path): Contains species and their corresponding character states.
- **Prompt Message** (prompt_file_path): Instructions for the API model. This file can be adjusted based on specific requirements.
* **Character Information** (character_file_path): Since the matrix typically lacks detailed descriptions, character mapping is necessary to obtain taxonomically meaningful descriptions.

> ### Usage
To utilize the TaxonGPT.py file effectively, a configuration file is required. This configuration file should include the necessary input file paths and the output file path. The essential information within the config file includes:
* **API Key**: Your OpenAI API key.
* **Paths**: A dictionary containing the paths to the input and output files.
```python
{
    "api_key": "YOUR API KEY HERE",
    "nexus_file_path": "<Full path to the input Nexus file>",
    "csv_output_path": "<Full path to the output CSV output file>",
    "json_output_path": "<Full path to the JSON output file>",
    "prompt_file_path": "<Full path to the input Prompt file>",
    "character_file_path": "<Full path to the input character info>"
}
```
To generate taxonomic results efficiently, ensure the configuration file contains the correct file paths. Based on the specific requirements for generating classification results, different branch functions can be used.
```python
# Example usage
config_file_path = "path/to/config.json"
taxon_gpt = TaxonGPT(config_file_path)

# Use paths from the configuration
# Generate the Taxonomic Key results
taxon_gpt.process_key(taxon_gpt.paths["nexus_file_path"], taxon_gpt.paths["prompt_file_path"], taxon_gpt.paths["character_file_path"])
# Generate the Taxonomic Description results
taxon_gpt.process_description(taxon_gpt.paths["matrix_file_path"], taxon_gpt.paths["character_file_path"], taxon_gpt.paths["output_file_path"], taxon_gpt.paths["prompt_file_path"])
```
#### ⚠️Caution: Refrain from disclosing your API key to unauthorized individuals or posting it in publicly accessible locations.

## Acknowledgements
