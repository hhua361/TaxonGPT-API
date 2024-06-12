import re

# 矩阵信息
matrix_info = {
    "Lytopylus bradzlotnicki": "23222112312",
    "Lytopylus colleenhitchcockae": "821211223(12)(12)",
    "Lytopylus flavicalcar": "5222(12)(12)22222",
    "Lytopylus gregburtoni": "7221112232(12)",
    "Lytopylus jessicadimauroae": "92122222321",
    "Lytopylus jessiehillae": "(BC)212(12)121122",
    "Lytopylus macadamiae": "A212(12)222322",
    "Lytopylus mingfangi": "(BC)222(12)121122",
    "Lytopylus rebeccashapleyae": "33222112(13)21",
    "Lytopylus robpringlei": "62122(12)22322",
    "Lytopylus sandraberriosae": "41-22112(13)22",
    "Lytopylus vaughntani": "1222111232(12)"
}

# 树结构
tree_structure = "(1:1,(((((((2:1,((5:2,10:0):0,7:1):2):2,3:1):0,4:2):0,(6:1,8:0):3):2,12:0):2,11:1):1,9:2):1)"

# taxa名称与编号的对应关系
taxa_labels = {
    "1": "Lytopylus_bradzlotnicki",
    "2": "Lytopylus_colleenhitchcockae",
    "3": "Lytopylus_flavicalcar",
    "4": "Lytopylus_gregburtoni",
    "5": "Lytopylus_jessicadimauroae",
    "6": "Lytopylus_jessiehillae",
    "7": "Lytopylus_macadamiae",
    "8": "Lytopylus_mingfangi",
    "9": "Lytopylus_rebeccashapleyae",
    "10": "Lytopylus_robpringlei",
    "11": "Lytopylus_sandraberriosae",
    "12": "Lytopylus_vaughntani"
}

# 将taxa替换为特征数组
def replace_taxa_with_features(tree, labels, matrix):
    pattern = re.compile(r'\b(\d+)\b')
    def replace_match(match):
        taxa_num = match.group(1)
        taxa_name = labels.get(taxa_num)
        if taxa_name:
            taxa_name = taxa_name.replace('_', ' ')
            features = matrix.get(taxa_name, '')
            return f"{taxa_name}[{features}]"
        return match.group(0)
    return pattern.sub(replace_match, tree)

# 执行替换
new_tree_structure = replace_taxa_with_features(tree_structure, taxa_labels, matrix_info)
print(new_tree_structure)
