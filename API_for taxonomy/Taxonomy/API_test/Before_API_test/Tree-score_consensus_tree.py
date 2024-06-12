
import dendropy

# Define two simple trees
tree1 = dendropy.Tree.get(
    path="D:/桌面/taxonomy_primary_result/The_GPT-4_result/Dataset_3 (The Lycopodiales (Diphasiastrum, Huperzia, Isoetes, Lycopodium, Selaginella)) 4/DELTA_data/Tree/consensus.tre",
    schema="nexus")
tree2 = dendropy.Tree.get(
    path="D:/桌面/taxonomy_primary_result/The_GPT-4_result/Dataset_3 (The Lycopodiales (Diphasiastrum, Huperzia, Isoetes, Lycopodium, Selaginella)) 4/GPT-4_new_generate/Tree/consensus.tre",
    schema="nexus",
    taxon_namespace=tree1.taxon_namespace)

# Function to perform and count rotations (a simple transformation)
def count_rotations(t1, t2):
    # Find the first difference in topology
    for node1, node2 in zip(t1.traverse(), t2.traverse()):
        if node1.is_leaf() or node2.is_leaf():
            continue
        # Compare children names sorted alphabetically
        children1 = sorted(child.name for child in node1.get_children() if child.name)
        children2 = sorted(child.name for child in node2.get_children() if child.name)
        if children1 != children2:
            # Perform a rotation
            node1.children.reverse()  # This is a simple rotation
            print(f"Rotation at node: {node1.name}")
            return 1  # Return the count of this rotation
    return 0

# Compare trees and count rotations
rotation_count = count_rotations(tree1, tree2)
print(f"Total rotations needed: {rotation_count}")
