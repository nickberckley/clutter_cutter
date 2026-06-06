import bpy
from .constants import PURGEABLE_TYPES


#### ------------------------------ /list/ ------------------------------ ####

def count_orphans(data_type) -> int:
    """Returns number of unused (orphaned) data for a specified data type."""

    data_collection = getattr(bpy.data, data_type)

    orphaned_count = 0
    for block in data_collection:
        if not block.users:
            orphaned_count += 1

    return orphaned_count


def list_orphans() -> list:
    """Returns the list of all orphaned data-blocks in the file."""

    orphans = []

    data_collection = [getattr(bpy.data, item[0]) for item in PURGEABLE_TYPES]
    for data_type in data_collection:
        for block in data_type:
            if block.users == 0:
                orphans.append(block)

    return orphans, len(orphans)


def find_collection_by_id(id):
    # NOTE: We handle node groups separately because their type can change based on editor.
    if isinstance(id, bpy.types.NodeTree):
        return bpy.data.node_groups

    collection = next(c for c in bpy.data.rna_type.properties
                      if hasattr(c, 'fixed_type') and c.fixed_type == id.rna_type)
    collection = getattr(bpy.data, collection.identifier)

    return collection


#### ------------------------------ /operate/ ------------------------------ ####


def purge_orphans(data_type, recursive=False) -> int:
    """Purges userless data for a specified data type."""

    data_collection = getattr(bpy.data, data_type)

    # "Cache" orphaned data-blocks before purging.
    if recursive:
        orphans_before, num_orphans_before = list_orphans()

    purged_count = 0
    for block in data_collection:
        if block.users == 0:
            if block.name == "Viewer Node":
                continue

            if recursive:
                orphans_before.remove(block)
                num_orphans_before - 1
            data_collection.remove(block)
            purged_count += 1

    # Get the list of orphans after purging and compare to "cache".
    recursive_count = 0
    if recursive:
        while True:
            orphans_after, num_orphans_after = list_orphans()
            new_orphans = [d for d in orphans_after if d not in orphans_before]

            if not new_orphans:
                break

            for block in new_orphans:
                collection = find_collection_by_id(block)
                try:
                    collection.remove(block)
                    recursive_count += 1
                except:
                    continue

            orphans_before = orphans_after

    return purged_count, recursive_count
