bl_info = {
    "name": "Clutter Cutter",
    "author": "Nika Kutsniashvili (nickberckley)",
    "version": (3, 0),
    "blender": (4, 2, 0),
    "location": "Outliner Header; File > Clean Up; File > External Data",
    "description": "Purge orphaned data by type, name, or suffixes. Pack & unpack images by name, and more.",
    "doc_url": "https://blendermarket.com/l/products/deep-clean", 
    "tracker_url": "https://blenderartists.org/t/purge-orphans-by-data-type/1448384",
    "category": "Utility"
}

import bpy
from . import(
    functions,
    operators,
    ui,
)


#### ------------------------------ REGISTRATION ------------------------------ ####

modules = [
    operators,
    ui,
]

def register():
    for module in modules:
        module.register()

def unregister():
    for module in modules:
        module.unregister()

if __name__ == "__main__":
    register()
