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
