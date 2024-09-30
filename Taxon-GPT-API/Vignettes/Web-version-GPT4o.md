Web version GPT-4o: Investgateing the GPT model application with Taxonomy 
====
## Introduction
Taxonomy, as a branch of systematics, has a crucial place in all biological disciplines. Accurate taxonomic information is essential for taxonomists to analyse evolutionary relationships between species, assess morphological features and name new species. However, this process relies heavily on natural language and requires extensive manual processing of taxonomic data, consuming significant time and human resources. Large-scale language models (LLMs) excel in natural language processing (NLP). In this manuscript, we demonstrate that the GPT-4o model is an efficient LLM that can efficiently process natural language in taxonomic studies and generate taxonomically meaningful results using relevant data. We tested the use of the **Web-based version of the GPT-4o** model in the field of taxonomy for generating taxonomic results and transforming taxonomic data.
## User interface
![web-markdown](https://github.com/user-attachments/assets/b3aa77b3-2770-4ab8-b954-208a1452964d)

## Prompt
Prompt design is critical in the use of the web version of GPT-4o. For different categorization tasks, content-specific Prompts are required, while flexible Prompts can be used to give accurate instructions by adjusting them to the right specifications.
>### Taxonomic Key
```
Using the prompt for Web version of GPT-4o to generate Taxonomic Key.

Prompt: Generation of Taxonomic key from Morphological Matrix
    I need to generate a taxonomic key using a morphological matrix provided in a CSV file. This matrix contains character states for various taxa. The goal is to determine the characters that best separate the taxa based on their states and progressively categorize them to construct the taxonomic key. The analysis should use information gain to evaluate each character's ability to classify the taxa evenly.
Please follow these requirements during the analysis:
    1. Initial Character Selection: Ensure all taxa have a defined state ('Missing' or 'Not applicable' is an invalid status) for the first character. Ignore characters with more than two states type and use information gain to select the most suitable character for initial classification.
    2. Dynamic Character Selection: For each new character selection, reload the original matrix. Re-evaluate the presence of invalid states in character, Ignore characters with missing or not applicable states for the current subset of taxa. Include characters with actual states for the taxa being considered, even if they have missing or not applicable states for other taxa.
    3. Character Selection Preference: Prefer characters with fewer state types when multiple characters have the same information gain. Ignore characters with more than three state types regardless of their information gain.
    4. Step-by-Step Classification: Classify taxa step-by-step according to the above rules until all taxa are individually classified. Display the results in a nested structure without showing the code implementation.

Refinement Prompts:
After generating the taxonomic key, need to add the corresponding CHARACTER and STATE information, perform character mapping, based on the corresponding CHARACTER's STATE that is provided to you, where "," is used to indicate that more than one state exists at the same time for the same CHARACTER(such as the character1 1,2 means both this taxa for the character 1 both have state 1 and state 2), and finally keep the numerical labeling
```
>### Taxonomic Description
```
Using the prompt for Web version of GPT-4o to generate Taxonomic Description.

Prompt: Generation of Taxonomic Descriptions from Morphological Matrix
Based on the provided morphological matrix (presented as a knowledge graph in JSON format), standard taxonomic descriptions are generated for all taxa in the matrix. Additional character labels and state labels will be provided, these labels contain a detailed description of each character and its corresponding state. Multiple states in the matrix (e.g., "1 and 2") indicate that the character of that species has both state 1 and state 2.
Specific requirements:
    1. Generate standard academic taxonomic descriptions, which need to include all characters in the morphological matrix and accurately correspond to the state of each character.
    2. Generate descriptions in list form and paragraph form. In paragraph form, the number of each character should be indicated.
Due to the large number of results, to avoid space constraints, please show the taxonomic description of each taxa separately.
```
>### Flexible adjust prompt
```
Flexible adjust prompt to generate the expect Taxonomic results.
Selects the specified character or species:

When inputting a prompt to generate Taxonomic keys or Taxonomic descriptions, if you need to adjust the expected results flexibly, you can append the following prompts:
Prompts:
    In the generated taxonomic results, I only want to select the following species (e.g., species1, species2, etc.) to generate taxonomic keys or taxonomic descriptions. Please strictly follow the above requirements and accurately select the corresponding species.
    In the generated taxonomic results, I only want to select the following characters (e.g., character1, character2, etc.) to generate taxonomic keys or taxonomic descriptions. Please strictly follow the above requirements and accurately select the corresponding characters.
```
## Overview
In the web version of GPT-4o, it is not possible to read Nexus files directly and the recognition of this file type is poor. Therefore, when passing morphological matrix information to the web version of GPT-4o, the Nexus file needs to be converted to Knowledge Graph or CSV format for input.
>### Input file
* **Nexus file example**
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
- **Knowledge graph example**
 ```
This is just an example of the part of knowledge graph format morphological matrix that will be shown.
{
    "Equisetum_arvense": {
        "Characteristics": {
            "Character1": "state 1 and  state 2",
            "Character2": "state 1",
            "Character3": "state 2",
            "Character4": "state 1 and  state 2",
            "Character5": "state 1",
            "Character6": "state 2",
            "Character7": "state 1",
            "Character8": "state 2",
            "Character9": "Missing",
            "Character10": "state 2",
            "Character11": "state 2",
            "Character12": "state 1 and  state 2",
            "Character13": "state 2",
            "Character14": "state 1",
            "Character15": "Missing",
            "Character16": "state 1",
            "Character17": "Missing",
            "Character18": "state 1",
            "Character19": "state 2",
            "Character20": "state 2 and  state 3",
            "Character21": "state 1",
            "Character22": "state 2",
            "Character23": "state 1",
            "Character24": "state 2",
            "Character25": "state 1",
            "Character26": "state 1",
            "Character27": "state 1",
            "Character28": "state 1",
            "Character29": "state 3"
        }
    },
    .........
```
* **Csv table example**
```markdown
| Species           | Character 1         | Character 2 | ... |
|-------------------|---------------------|-------------|-----|
| Equisetum_arvense | state 1 and state 2 | state 1     | ... |
| ...               | ...                 | ...         | ... |
```

>### Usage
>Send the message by providing the corresponding prompt information and related content files to the interface of the web version of GPT-4o, and then wait for the result of the response from the web version of GPT-4o.
## Example
>### Taxonomic Key
>The taxonomic key results generated using the TaxonGPT.Key function are derived from the Equisetum dataset extracted from the DELTA database. This dataset includes 12 species characterized by 29 morphological traits, stored in the form of a Nexus matrix.
```
Character22
	• 1
		○ Character5
			§ 2: Diphasiastrum_alpinum
			§ 3: Diphasiastrum_complanatum
			§ 1
				□ Character16
					® Not Applicable: Huperzia_selago
					® 1
						◊ Character20
							} 1: Lycopodiella_inundata
							} 2,3: Lycopodium_annotinum
					® 2: Lycopodium_clavatum
	• 3
		○ Character18
			§ 2: Isoetes_echinospora
			§ 3: Isoetes_histrix
			§ 1: Isoetes_lacustris
	• 2
		○ Character4
			§ 1: Selaginella_kraussiana
			§ 2: Selaginella_selaginoides
```
>### Taxonomic Description
>The dataset results generated using the TaxonGPT. Description function include detailed information for one of the species, Equisetum arvense. This data is derived from the Equisetum dataset extracted from the DELTA database, which comprises 12 species characterized by 29 morphological characters, stored in the form of a Nexus matrix.
```
Taxonomic Description for Equisetum arvense
List Form
	1. Character 1: The rhizomes - Bearing tubers and Not tuberous
	2. Character 2: The shoots - Conspicuously dimorphic: the cone-bearing stems thick, unbranched, brown and non-assimilating, appearing in early spring and withering before the emergence of the sterile, branched, green, persistent ones
	3. Character 3: The brown, non-assimilating fertile stems - With only 4 to 6 relatively distant sheaths
	4. Character 4: The main stems - Erect and Decumbent
	5. Character 5: The main stems - Bright green
	6. Character 6: The main stems - Slightly rough
	7. Character 7: The main stems - Bearing whorls of slender branches at the nodes
	8. Character 8: The main stems - Dying down in autumn
	9. Character 9: The main stem internodes - Missing
	10. Character 10: The longitudinal internodal grooves - Deep, with prominent ridges between
	11. Character 11: The main stem internodes - With a central hollow
	12. Character 12: Central hollow - Much less than half the diameter of the internode and About half the diameter of the internode
	13. Character 13: Endodermis - Comprising a single layer outside the ring of vascular bundles
	14. Character 14: The main stem sheaths - About as broad as long
	15. Character 15: The main stem sheaths - Missing
	16. Character 16: The teeth - Ribbed
	17. Character 17: The teeth - Missing
	18. Character 18: The primary branching - Symmetrical
	19. Character 19: The primary branches - Numerous
	20. Character 20: The primary branches - Spreading and Drooping
	21. Character 21: The primary branches - Simple
	22. Character 22: The first primary branch internodes - At least as long as the subtending sheaths, at least on the upper parts of the stem
	23. Character 23: The primary branch internodes - Solid
	24. Character 24: Stomata - Not sunken
	25. Character 25: The cones - Blunt
	26. Character 26: Spores - Fertile
	27. Character 27: Spores released - April
	28. Character 28: Subgenus - Equisetum
	29. Character 29: Section - Vernalia

Paragraph Form
The rhizomes of Equisetum arvense are both bearing tubers and not tuberous (Character 1). The shoots are conspicuously dimorphic: the cone-bearing stems thick, unbranched, brown and non-assimilating, appearing in early spring and withering before the emergence of the sterile, branched, green, persistent ones (Character 2). The brown, non-assimilating fertile stems have only 4 to 6 relatively distant sheaths (Character 3). The main stems are both erect and decumbent (Character 4) and are bright green (Character 5). The main stems are slightly rough (Character 6) and bear whorls of slender branches at the nodes (Character 7). The main stems die down in autumn (Character 8). The main stem internodes are missing (Character 9). The longitudinal internodal grooves are deep, with prominent ridges between (Character 10). The main stem internodes have a central hollow (Character 11), which is much less than half the diameter of the internode and about half the diameter of the internode (Character 12). The endodermis comprises a single layer outside the ring of vascular bundles (Character 13). The main stem sheaths are about as broad as long (Character 14). The main stem sheaths are missing (Character 15). The teeth are ribbed (Character 16) and are missing (Character 17). The primary branching is symmetrical (Character 18). The primary branches are numerous (Character 19) and are both spreading and drooping (Character 20). The primary branches are simple (Character 21). The first primary branch internodes are at least as long as the subtending sheaths, at least on the upper parts of the stem (Character 22). The primary branch internodes are solid (Character 23). The stomata are not sunken (Character 24). The cones are blunt (Character 25). The spores are fertile (Character 26) and are released in April (Character 27). The subgenus is Equisetum (Character 28). The section is Vernalia (Character 29).
```
