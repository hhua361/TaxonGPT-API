TaxonGPT: Efficient Taxonomic Data Conversion and Key Generation with GPT-4o model
====

## Introduction
Taxonomy, as a branch of systematics, holds critical importance across various biological disciplines. Accurate taxonomic information is essential for taxonomists to analyze evolutionary relationships between species, assess morphological characteristics, and name new species. However, this process heavily relies on natural language and involves extensive manual work to handle taxonomic data, consuming significant time and human resources. Large Language Models (LLMs) have demonstrated excellent performance in Natural Language Processing (NLP). In this manuscript, we demonstrated the GPT-4o model, a efficient LLM, can effectively handling natural language in taxonomic research, using relevant data to generate taxonomically meaningful results. We developed the <strong>TaxonGPT (API)</strong> function, which utilizes the GPT-4o model to process Nexus matrix data, converting it into taxonomic keys and taxonomic descriptions, providing an innovative automated approach to taxonomic data processing.

## Installation

## Overview
> ### Input file
TaxonGPT is dedicated to converting information from Nexus matrices into biologically meaningful taxonomic information and accurate natural language descriptions of species. To achieve comprehensive taxonomic data, the input files for TaxonGPT include:
* **Nexus Matrix**: Contains species and their corresponding character states.
- **Prompt Message**: Instructions for the API model. This file can be adjusted based on specific requirements.
* **Character Information**: Since the matrix typically lacks detailed descriptions, character mapping is necessary to obtain taxonomically meaningful descriptions.

> ### Usage
To utilize the TaxonGPT.py file effectively, a configuration file is required. This configuration file should include the necessary input file paths and the output file path. The essential information within the config file includes:
* **API Key**: Your OpenAI API key.
* **Paths**: A dictionary containing the paths to the input and output files.
```python
{
    "api_key": "your_openai_api_key",
    "paths": {
        "nexus_file_path": "path/to/nexus_file.nex",
        "prompt_file_path": "path/to/prompt_messages.json",
        "character_file_path": "path/to/character_info.json",
        "matrix_file_path": "path/to/matrix_knowledge_graph.json",
        "output_file_path": "path/to/taxonomic_descriptions.json"
    }
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

## Example
