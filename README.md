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
    "prompt_file_path": "<Full path to the input Prompt file>",
    "character_file_path": "<Full path to the input character info file>",
    
    "csv_output_path": "<Full path to  output CSV format matrix file>",
    "json_output_path": "<Full path to output JSON format matrix file>",
    "taxonomic_description_path": "<Full path to output taxonomic description file>"
    "taxonomic_key_path": "<Full path to output taxonomic key file>"

    
    "comparison_output_path": "<Full path to output taxonomic key file>",
    # By default, the description check feature is disabled to prevent generating excessive redundant results. If you need to check the execution steps, please set "enable_description_check": false to true in the configuration file.
    "enable_description_check": false

}
```
To generate taxonomic results efficiently, ensure the configuration file contains the correct file paths. Based on the specific requirements for generating classification results, different branch functions can be used.
```python
# Through TaxonGPT() to generate the related result
TaxonGPT = TaxonGPT(config_file_path)

# Generate the Taxonomic Key
TaxonGPT.process_key()

# Generate the Taxonomic Description
TaxonGPT.process_description()
```
#### ⚠️Caution: Refrain from disclosing your API key to unauthorized individuals or posting it in publicly accessible locations.

## Acknowledgements
Sincerely thank OpenAI for their development of the ChatGPT and ChatGPT-4o models, which provided valuable assistance during this research and the preparation of the manuscript. Special appreciation is extended to Andrea Grecu, June Ko, and Miao Wang for their support and insightful discussions. The ChatGPT-4o model's API was particularly instrumental in conducting the experiments. Additionally, the ChatGPT-4o model assisted in the editing of this paper, including grammar and syntax corrections.
