TaxonGPT: Efficient Taxonomic Data Conversion and Key Generation with GPT-4o model
====

## Introduction
Taxonomy, as a branch of systematics, holds critical importance across various biological disciplines. Accurate taxonomic information is essential for taxonomists to analyze evolutionary relationships between species, assess morphological characteristics, and name new species. However, this process heavily relies on natural language and involves extensive manual work to handle taxonomic data, consuming significant time and human resources. Large Language Models (LLMs) have demonstrated excellent performance in Natural Language Processing (NLP). In this manuscript, we demonstrated the GPT-4o model, a efficient LLM, can effectively handling natural language in taxonomic research, using relevant data to generate taxonomically meaningful results. We developed the <strong>TaxonGPT (API)</strong> function, which utilizes the GPT-4o model to process Nexus matrix data, converting it into taxonomic keys and taxonomic descriptions, providing an innovative automated approach to taxonomic data processing.

## Installation
To use the TaxonGPT function, you can download the TaxonGPT.py file located in the main directory. Then, run it in your local Python environment.

TaxonGPT can be installed by following this instruction on Github.\
TaxonGPT depends on the Python package openai, please make sure it is installed as well.

https://github.com/hhua361/Taxon-GPT-API.git/Taxonomy/TaxonGPT.py
 ### Steps:
1. To use the TaxonGPT function, you can download the TaxonGPT.py file located in the main directory. Then, run it in your local Python environment.
2. Ensure you have Python installed on your system.
3. Run the following command in your terminal to execute the file:

```
python path/to/TaxonGPT.py
```
## Obtain the OpenAI API key and configure it as an environment variable
To integrate the TaxonGPT function, the OpenAI API (Application Programming Interface) must be utilized. Connecting to the OpenAI API can invoking relevant models provided by OpenAI. Since the API key is a sensitive and confidential code, it is crucial to prevent exposing the key or submitting it through a browser.To ensure the API key is securely imported and avoid any potential risk, it is mandatory to set the API key as a system environment variable before using the TaxonGPT function.

If the API key is correctly set, the TaxonGPT function will proceed with the subsequent operations. However, if the API key is not properly loaded into the environment, the TaxonGPT function will return an appropriate prompt, providing instructions to help check and resolve the issues.

### How to Correctly Obtain and Use OpenAI's API Key:
1. Locate the "API" section at the bottom of the OpenAI interface.
2. Log in to your user account through the API login portal and navigate to the API interface.
3. Click on the "Dashboard" located at the top right corner.
4. Access the "API keys" interface to manage your API keys.
5. Create the API key and ensure to save and record this key properly for future use.

![step1-4](https://github.com/user-attachments/assets/b17b1c8e-d233-40e4-a0dd-c8a8683bdde1)
#### ⚠️Caution: Refrain from disclosing your API key to unauthorized individuals or posting it in publicly accessible locations.
## Overview
> ### Input file
> TaxonGPT is dedicated to converting information from Nexus matrices into biologically meaningful taxonomic information and accurate natural language descriptions of species. To achieve comprehensive taxonomic data, the input files for TaxonGPT include:
* **Nexus Matrix** (nexus_file_path): Contains species and their corresponding character states.
```
This is just an example of the Nexus file format that will be shown.
MATRIX 
'Equisetum arvense'                                                             
(12)12(12)1212?22(12)21?1?12(23)121211113                                       
'Equisetum fluviatile'                                                          
(12)3-1?3(13)2?1231?(12)2?2211?2211(34)11                                       
'Equisetum hyemale'                                                             
23-121311?2(23)312?2------121(45)2-                                             
'Equisetum litorale'                                                          
13-1?212?12(12)1?12?(12)211(12)2212-11                                          
'Equisetum moorei'                                                            
23-121322?2(23)?21?1------122-2-                                                
'Equisetum palustre'                                                            
13-(12)?2(123)222212?111(12)(12)(12)112211(234)11                               
'Equisetum pratense'                                                            
22?1?1(13)2??2(23)2???112(23)121211112                                          
'Equisetum ramosissimum'                                                        
23-??(12)112?2(23)3???1?2??12121(2345)2-                                        
'Equisetum sylvaticum'                                                          
(12)2?11(23)(13)22?2(23)2??11123221211(12)12                                    
'Equisetum telmateia'                                                           
(12)111??12212(23)2?111122111211112                                             
'Equisetum trachyodon'                                                        
23-(12)?1(23)12?213?211???1??122-2-                                             
'Equisetum variegatum'                                                          
23-(12)?2(23)12?213?111???1??121(45)2-                                                                                       
;
```
* **Character Information** (character_file_path): Since the matrix typically lacks detailed descriptions, character mapping is necessary to obtain taxonomically meaningful descriptions.
```
This is just an example of the character information format that will be shown.
{
    "1": {
        "description": "The rhizomes <whether tuberous>",
        "states": {
            "1": "Bearing tubers",
            "2": "Not tuberous"
        }
    },
    "2": {
        "description": "The shoots <dimorphism>",
        "states": {
            "1": "Conspicuously dimorphic: the cone-bearing stems thick, unbranched, brown and non-assimilating, appearing in early spring and withering before the emergence of the sterile, branched, green, persistent ones",
            "2": "Distinguishable as fertile and sterile: both types produced at the same time, but those bearing cones remaining non-green and unbranched until after spore dispersal, and only later becoming green and branching so as to resemble the sterile stems vegetatively",
            "3": "All green and alike vegetatively, the sterile and cone-bearing shoots emerging at the same time"
        }
    },
    .........
```
- **Prompt Message** (prompt_file_path): Instructions for the API model. This file can be adjusted based on specific requirements.
> ### Usage
>To utilize the TaxonGPT.py file effectively, a configuration file is required. This configuration file should include the necessary input file paths and the output file path. The essential information within the config file includes:
>* **API Key**: Your OpenAI API key.
>* **Paths**: A dictionary containing the paths to the input and output files.
```
This is just an example of the config file format that will be shown.
"""
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
"""
```

To generate taxonomic results efficiently, ensure the configuration file contains the correct file paths. Based on the specific requirements for generating classification results, different branch functions can be used.
```
# Example usage
config_file_path = "path/to/config.json"
# Through TaxonGPT() to generate the related result
TaxonGPT = TaxonGPT(config_file_path)

# Generate the Taxonomic Key
TaxonGPT.process_key()
# Generate the Taxonomic Description
TaxonGPT.process_description()
```

## Example
> ### Taxonomic Key
> The taxonomic key results generated using the TaxonGPT.Key function are derived from the *Equisetum* dataset extracted from the DELTA database. This dataset includes 12 species characterized by 29 morphological traits, stored in the form of a Nexus matrix.

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
    -  The main stems <of the assimilating shoots, rough or smooth>: Slightly rough ........ Equisetum variegatum
```
> ### Taxonomic Description
> The dataset results generated using the TaxonGPT. Description function include detailed information for one of the species, *Equisetum arvense*. This data is derived from the *Equisetum* dataset extracted from the DELTA database, which comprises 12 species characterized by 29 morphological characters, stored in the form of a Nexus matrix.

```
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
