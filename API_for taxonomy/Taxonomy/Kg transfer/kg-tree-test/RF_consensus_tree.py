import dendropy
# read the tree form the NEXSU file
tree1 = dendropy.Tree.get(
    path="D:/桌面/taxonomy_primary_result/The_GPT-4_result/Dataset_3 (The Lycopodiales (Diphasiastrum, Huperzia, Isoetes, Lycopodium, Selaginella)) 4/DELTA_data/Tree/consensus.tre",
    schema="nexus"
)
tree2 = dendropy.Tree.get(
    path="D:/桌面/taxonomy_primary_result/The_GPT-4_result/Dataset_3 (The Lycopodiales (Diphasiastrum, Huperzia, Isoetes, Lycopodium, Selaginella)) 4/GPT-4_new_generate/Tree/consensus.tre",
    schema="nexus",
    taxon_namespace=tree1.taxon_namespace
)
# calulate the RF distance
rf_distance = dendropy.calculate.treecompare.symmetric_difference(tree1, tree2)
# print the RF distance
print("Robinson-Foulds Distance:", rf_distance)

# only calculate the RF distance can not accuccrcy evaluate the result, so we need to consider the ratios of nodes
num_leaves = len(tree2.leaf_nodes())
print("leaf_nodes:", num_leaves)
max_rf_distance = 2 * (num_leaves - 3)
print("Maximum RF distance for the tree:", max_rf_distance)