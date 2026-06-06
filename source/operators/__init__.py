if "bpy" in locals():
    import importlib
    for mod in [pack_images,
                purge_by_name,
                purge_by_type,]:
        importlib.reload(mod)
else:
    import bpy
    from . import (
        pack_images,
        purge_by_name,
        purge_by_type,
    )


#### ------------------------------ REGISTRATION ------------------------------ ####

modules = [
    pack_images,
    purge_by_name,
    purge_by_type,
]

def register():
    for module in modules:
        module.register()

def unregister():
    for module in reversed(modules):
        module.unregister()
