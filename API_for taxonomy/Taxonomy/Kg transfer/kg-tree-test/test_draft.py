import re

# 定义矩阵信息
matrix_info_str = """
Equisetum_arvense       (12)12(12)1212?22(12)21?1?12(23)121211113
Equisetum_fluviatile    (12)3-1?3(13)2?1231?(12)2?2211?2211(34)11
Equisetum_hyemale       23-121311?2(23)312?2------121(45)2-
Equisetum_litorale    13-1?212?12(12)1?12?(12)211(12)2212-11
Equisetum_moorei      23-121322?2(23)?21?1------122-2-
Equisetum_palustre      13-(12)?2(123)222212?111(12)(12)(12)112211(234)11
Equisetum_pratense      22?1?1(13)2??2(23)2???112(23)121211112
Equisetum_ramosissimum  23-??(12)112?2(23)3???1?2??12121(2345)2-
Equisetum_sylvaticum    (12)2?11(23)(13)22?2(23)2??11123221211(12)12
Equisetum_telmateia     (12)111??12212(23)2?111122111211112
Equisetum_trachyodon  23-(12)?1(23)12?213?211???1??122-2-
Equisetum_variegatum    23-(12)?2(23)12?213?111???1??121(45)2-
Extinct_Sphenopsida     ?--???????2??????------??--?-
node9	13(12)1(12)212212211121(12)21112211(34)11
node8	13(12)1(12)2122(12)2221111(12)2(12)112211(34)11
node16	 23(12)121312(12)2231211(12)2(12)11212(12)42(12)
node15	 23(12)121312(12)2231111(12)2(12)11212(12)42(12)
node14	 23(12)1(12)2312(12)2231111(12)2(12)11212142(12)
node13	 23(12)1(12)2112(12)2231111(12)2(12)112121(34)2(12)
node7	 23(12)1(12)2122(12)2221111(12)2(12)112211(34)1(12)
node6	 2(34)(12)1(12)2122(12)2221111(12)2(12)11(12)211(1234)1(12)
node5	 21(12)1(12)2122(12)2221111122111211112
node24	 22(12)112122(12)222111112(23)121211112
node4	 21(12)112122(12)222111112(23)121211112
node2	 21(12)112122(12)222111112(23)12121111(23)
"""

# 将矩阵信息转换为字典
matrix_info = {}
for line in matrix_info_str.strip().split('\n'):
    parts = line.split(maxsplit=1)
    if len(parts) == 2:
        matrix_info[parts[0]] = parts[1]

# 树结构
tree_structure = "(1:3.0,((((((2:2.0,4:1.0)node9:2.0,6:2.0)node8:1.0,((((3:3.0,11:1.0)node16:1.0,,:2.0)node15:2.0,12:1.0)node14:1.0,8:0.0)node13:5.0)node7:0.0,13:0.0)node6:8.0,10:0.0)node5:2.0,(7:1.0,9:1.0)node24:2.0)node4:0.0)node2"

# taxa名称与编号的对应关系
taxa_labels = {
    "1": "Equisetum_arvense",
    "2": "Equisetum_fluviatile",
    "3": "Equisetum_hyemale",
    "4": "Equisetum_litorale",
    "5": "Equisetum_moorei",
    "6": "Equisetum_palustre",
    "7": "Equisetum_pratense",
    "8": "Equisetum_ramosissimum",
    "9": "Equisetum_sylvaticum",
    "10": "Equisetum_telmateia",
    "11": "Equisetum_trachyodon",
    "12": "Equisetum_variegatum",
    "13": "Extinct_Sphenopsida"
}

# 将taxa替换为特征数组
def replace_taxa_with_features(tree, labels, matrix):
    pattern = re.compile(r'\b(\d+|node\d+)\b')
    def replace_match(match):
        taxa_num = match.group(1)
        taxa_name = labels.get(taxa_num) if not taxa_num.startswith('node') else taxa_num
        if taxa_name:
            features = matrix.get(taxa_name, '')
            return f"{taxa_name}[{features}]"
        return match.group(0)
    return pattern.sub(replace_match, tree)

# 执行替换
new_tree_structure = replace_taxa_with_features(tree_structure, taxa_labels, matrix_info)
print(new_tree_structure)
