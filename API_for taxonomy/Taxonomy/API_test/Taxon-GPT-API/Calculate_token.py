import tiktoken

def count_tokens(text, model="gpt-4"):
    encoding = tiktoken.encoding_for_model(model)
    tokens = encoding.encode(text)
    return len(tokens)

def count_message_tokens(messages, model="gpt-4"):
    total_tokens = 0
    for message in messages:
        role_tokens = count_tokens(message['role'], model)
        content_tokens = count_tokens(message['content'], model)
        total_tokens += role_tokens + content_tokens
    return total_tokens

messages = [
    {
        "role": "system",
        "content": """### Taxonomic Description for Equisetum arvense

        #### List Form:
        1. The rhizomes: Bearing tubers and Not tuberous
        2. The shoots: Conspicuously dimorphic: the cone-bearing stems thick, unbranched, brown and non-assimilating, appearing in early spring and withering before the emergence of the sterile, branched, green, persistent ones
        3. The brown, non-assimilating fertile stems: With only 4 to 6 relatively distant sheaths
        4. The main stems: Erect and Decumbent
        5. The main stems: Bright green
        6. The main stems: Slightly rough
        7. The main stems: Bearing whorls of slender branches at the nodes
        8. The main stems: Dying down in autumn
        9. The main stem internodes: Missing
        10. The longitudinal internodal grooves: Deep, with prominent ridges between
        11. The main stem internodes: With a central hollow
        12. Central hollow: About half the diameter of the internode and More than half the diameter of the internode
        13. Endodermis: Comprising a single layer outside the ring of vascular bundles
        14. The main stem sheaths: About as broad as long
        15. The main stem sheaths: Missing
        16. The teeth: Ribbed
        17. The teeth: Missing
        18. The primary branching: Symmetrical
        19. The primary branches: Numerous
        20. The primary branches: Spreading and Drooping
        21. The primary branches: Simple
        22. The first branch internodes: At least as long as the subtending sheaths, at least on the upper parts of the stem
        23. The primary branch internodes: Solid
        24. Stomata: Not sunken
        25. The cones: Blunt
        26. Spores: Fertile
        27. Spores released: April
        28. Subgenus: Equisetum
        29. Section: Vernalia
        
        #### Paragraph Form:
        Equisetum arvense is characterized by the following features: (1) The rhizomes are both bearing tubers and not tuberous. (2) The shoots are conspicuously dimorphic, with the cone-bearing stems thick, unbranched, brown, and non-assimilating, appearing in early spring and withering before the emergence of the sterile, branched, green, persistent ones. (3) The brown, non-assimilating fertile stems have only 4 to 6 relatively distant sheaths. (4) The main stems are both erect and decumbent. (5) The main stems are bright green. (6) The main stems are slightly rough. (7) The main stems bear whorls of slender branches at the nodes. (8) The main stems die down in autumn. (9) The main stem internodes are missing. (10) The longitudinal internodal grooves are deep, with prominent ridges between. (11) The main stem internodes have a central hollow. (12) The central hollow is about half the diameter of the internode and more than half the diameter of the internode. (13) The endodermis comprises a single layer outside the ring of vascular bundles. (14) The main stem sheaths are about as broad as long. (15) The main stem sheaths are missing. (16) The teeth are ribbed. (17) The teeth are missing. (18) The primary branching is symmetrical. (19) The primary branches are numerous. (20) The primary branches are spreading and drooping. (21) The primary branches are simple. (22) The first branch internodes are at least as long as the subtending sheaths, at least on the upper parts of the stem. (23) The primary branch internodes are solid. (24) The stomata are not sunken. (25) The cones are blunt. (26) The spores are fertile. (27) The spores are released in April. (28) The subgenus is Equisetum. (29) The section is Vernalia."""
    }
]

total_tokens = count_message_tokens(messages)
print(f"Total tokens: {total_tokens}")

