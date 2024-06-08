import bpy


#### ------------------------------ /list/ ------------------------------ ####

def orphaned_counter(data_type):
    """Returns number of unused (orphaned) data for specified data type"""
    data_collection = getattr(bpy.data, data_type)

    orphaned_count = 0
    for block in data_collection:
        if not block.users:
            orphaned_count += 1

    return orphaned_count



#### ------------------------------ /operate/ ------------------------------ ####

def purge_unrecursive(data_type):
    """Purges unused data for specified data type (without recursion)"""
    data_collection = getattr(bpy.data, data_type)

    purged_count = 0
    for block in data_collection:
        if block.users == 0:
            if not block.name == "Viewer Node":
                data_collection.remove(block)
                purged_count += 1

    return purged_count


def purge_recursive_node_trees(nodes):
    recursive_count = 0
    popped_nodes = []

    # find_orphaned_blocks_in_node_tree
    orphaned_images = []
    orphaned_groups = []
    for node in nodes:
        if node.type == 'TEX_IMAGE':
            image = node.image
            if image and image.users == 1:
                orphaned_images.append(image)

        if node.type == 'GROUP':
            if node.node_tree and node.node_tree.users == 1:
                orphaned_groups.append(node)


    # find_orphaned_blocks_in_recursive_node_groups
    stack = [node.node_tree for node in orphaned_groups]
    while stack:
        tree = stack.pop()
        popped_nodes.append(tree)

        for node in tree.nodes:
            if node.type == 'TEX_IMAGE':
                image = node.image
                if image and image.users == 1:
                    orphaned_images.append(image)

            if node.type == 'GROUP' and node.node_tree.users == 1:
                stack.append(node.node_tree)


    # Purge Node Trees
    for group in popped_nodes:
        # print("Purged orphaned node group: " + group.name)
        bpy.data.node_groups.remove(group, do_unlink=True)
        recursive_count += 1

    for image in orphaned_images:
        # print("Purged orphaned node group: " + image.name)
        bpy.data.images.remove(image, do_unlink=True)
        recursive_count += 1

    return recursive_count
