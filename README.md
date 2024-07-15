TaxonGPT: Efficient Taxonomic Data Conversion and Key Generation with GPT-4o model
====

## Introduction
Taxonomy, as a branch of systematics, holds critical importance across various biological disciplines. Accurate taxonomic information is essential for taxonomists to analyze evolutionary relationships between species, assess morphological characteristics, and name new species. However, this process heavily relies on natural language and involves extensive manual work to handle taxonomic data, consuming significant time and human resources. Large Language Models (LLMs) have demonstrated excellent performance in Natural Language Processing (NLP). In this manuscript, we demonstrated the GPT-4o model, a efficient LLM, can effectively handling natural language in taxonomic research, using relevant data to generate taxonomically meaningful results. We developed the <strong>TaxonGPT (API)</strong> function, which utilizes the GPT-4o model to process Nexus matrix data, converting it into taxonomic keys and taxonomic descriptions, providing an innovative automated approach to taxonomic data processing.

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
![Taxon-GPT-flowchart](https://github.com/user-attachments/assets/75c3a8c1-7caf-497c-90b5-a65ed17af1c8)

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
    "api_key": "your_openai_api_key",
    "paths": {
        "nexus_file_path": "path/to/nexus_file.nex",
        "prompt_file_path": "path/to/prompt_messages.json",
        "character_file_path": "path/to/character_info.json",
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
> The taxonomic key results generated using the TaxonGPT.Key function are derived from the Equisetum dataset extracted from the DELTA database. This dataset includes 12 species characterized by 29 morphological traits, stored in the form of a Nexus matrix.

```markdown
1.
    -  The rhizomes <whether tuberous>: Bearing tubers ........ 2
    -  The rhizomes <whether tuberous>: Bearing tubers//Not tuberous ........ 3
    -  The rhizomes <whether tuberous>: Not tuberous ........ 4
2(1).
    -  The longitudinal internodal grooves <in the main stem internodes of the assimilating shoots, details>: Fine, the ribs between them not prominent ........ 5
    -  The longitudinal internodal grooves <in the main stem internodes of the assimilating shoots, details>: Deep, with prominent ridges between ........ Equisetum palustre
3(1).
    -  The shoots <dimorphism>: Conspicuously dimorphic ........ 7
    -  The shoots <dimorphism>: Distinguishable as fertile and sterile ........ Equisetum sylvaticum
    -  The shoots <dimorphism>: All green and alike vegetatively, the sterile and cone-bearing shoots emerging at the same time ........ Equisetum fluviatile
4(1).
    -  The main stems <of the assimilating shoots, persistence>: Persisting through the winter ........ 8
    -  The main stems <of the assimilating shoots, persistence>: Dying down in autumn ........ 9
5(2).
    -  Endodermis <in main stem internodes of assimilating shoots, location>: Surrounding the individual vascular bundles ........ 6
    -  Endodermis <in main stem internodes of assimilating shoots, location>: Comprising a single layer outside the ring of vascular bundles ........ Equisetum palustre
6(5).
    -  The main stems <of the assimilating shoots, carriage>: Erect ........ Equisetum litorale
    -  The main stems <of the assimilating shoots, carriage>: Erect//Decumbent ........ Equisetum palustre
7(3).
    -  The brown, non-assimilating fertile stems <number of sheaths>: With numerous sheaths and relatively short internodes ........ Equisetum telmateia
    -  The brown, non-assimilating fertile stems <number of sheaths>: With only 4 to 6 relatively distant sheaths ........ Equisetum arvense
8(4).
    -  The main stems <of the assimilating shoots, branching>: Bearing whorls of slender branches at the nodes ........ Equisetum ramosissimum
    -  The main stems <of the assimilating shoots, branching>: Sparingly branched, the branches solitary and similar to the main stem//Simple ........ 10
    -  The main stems <of the assimilating shoots, branching>: Simple ........ Equisetum hyemale
9(4).
    -  The shoots <dimorphism>: Distinguishable as fertile and sterile ........ Equisetum pratense
    -  The shoots <dimorphism>: All green and alike vegetatively, the sterile and cone-bearing shoots emerging at the same time ........ Equisetum moorei
10(8).
    -  The main stems <of the assimilating shoots, rough or smooth>: Very rough ........ Equisetum trachyodon
    -  The main stems <of the assimilating shoots, rough or smooth>: Slightly rough ........ Equisetum variegatum![image](https://github.com/user-attachments/assets/869a4ae3-a5cd-47b3-97e7-5bac10657ef5)
```

> The dataset results generated using the TaxonGPT.Description function include detailed information for one of the species, *Equisetum arvense*. This data is derived from the Equisetum dataset extracted from the DELTA database, which comprises 12 species characterized by 29 morphological traits, stored in the form of a Nexus matrix.

```python

Taxonomic Description for *Equisetum arvense*
Equisetum_arvense: 
	List Form:
	1. **The rhizomes**: Bearing tubers and Not tuberous
	2. **The shoots**: Conspicuously dimorphic
	3. **The brown, non-assimilating fertile stems**: With only 4 to 6 relatively distant sheaths
	4. **The main stems (of the assimilating shoots, carriage)**: Erect and Decumbent
	5. **The main stems (of the assimilating shoots, colour)**: Bright green
	6. **The main stems (of the assimilating shoots, rough or smooth)**: Slightly rough
	7. **The main stems (of the assimilating shoots, branching)**: Bearing whorls of slender branches at the nodes
	8. **The main stems (of the assimilating shoots, persistence)**: Dying down in autumn
	9. **The main stem internodes (of the assimilating shoots, whether swollen)**: Missing
	10. **The longitudinal internodal grooves (in the main stem internodes of the assimilating shoots, details)**: Deep,with prominent ridges between
	11. **The main stem internodes (of the assimilating shoots, presence of a central hollow)**: With a central hollow
	12. **Central hollow (of the main stem internodes of assimilating shoots, relative diameter)**: Much less than half the diameter of the internode and About half the diameter of the internode
	13. **Endodermis (in main stem internodes of assimilating shoots, location)**: Comprising a single layer outside the ring of vascular bundles
	14. **The main stem sheaths (of assimilating shoots, length relative to breadth)**: About as broad as long
	15. **The main stem sheaths (of assimilating shoots, loose or appressed)**: Missing
	16. **The teeth (of the main stem sheaths of assimilating shoots, ribbing)**: Ribbed
	17. **The teeth (of the main stem sheaths of assimilating shoots, persistence)**: Missing
	18. **The primary branching (regularity)**: Symmetrical
	19. **The primary branches (when present, few or many)**: Numerous
	20. **The primary branches (carriage)**: Spreading and Drooping
	21. **The primary branches (of assimilating shoots, whether themselves branched)**: Simple
	22. **The first (primary) branch internodes (of assimilating shoots, relative length)**: At least as long as the subtending sheaths, at least on the upper parts of the stem
	23. **The primary branch internodes**: Solid
	24. **Stomata (of assimilating shoots, insertion relative to the adjacent epidermal cells)**: Not sunken
	25. **The cones (blunt or apiculate)**: Blunt
	26. **Spores (whether fertile)**: Fertile
	27. **Spores released (months released)**: April
	28. **Subgenus**: Equisetum
	29. **Section (of subgenus Equisetum)**: Vernalia
	
	Paragraph Form:
	Equisetum arvense is characterized by rhizomes that are both bearing tubers and not tuberous (1). The shoots are conspicuously dimorphic (2). The brown, non-assimilating fertile stems have only 4 to 6 relatively distant sheaths (3). The main stems of the assimilating shoots are both erect and decumbent (4), and they are bright green in color (5). These stems are slightly rough (6) and bear whorls of slender branches at the nodes (7). The main stems die down in autumn (8). The longitudinal internodal grooves in the main stem internodes of the assimilating shoots are deep, with prominent ridges between (10). The main stem internodes have a central hollow (11), which is much less than half the diameter of the internode and about half the diameter of the internode (12). The endodermis in the main stem internodes of the assimilating shoots comprises a single layer outside the ring of vascular bundles (13). The main stem sheaths of the assimilating shoots are about as broad as long (14). The teeth of the main stem sheaths of the assimilating shoots are ribbed (16). The primary branching is symmetrical (18), and the primary branches are numerous (19). These branches are both spreading and drooping (20). The primary branches of the assimilating shoots are simple (21), and the first primary branch internodes are at least as long as the subtending sheaths, at least on the upper parts of the stem (22). The primary branch internodes are solid (23). The stomata of the assimilating shoots are not sunken relative to the adjacent epidermal cells (24). The cones are blunt (25). The spores are fertile (26) and are released in April (27). This species belongs to the subgenus Equisetum (28) and the section Vernalia (29).
```
## Acknowledgements
