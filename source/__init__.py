if "bpy" in locals():
    import importlib
    for mod in [operators,
                ui,
                ]:
        importlib.reload(mod)
    print("Add-on Reloaded: Clutter Cutter")
else:
    import bpy
    from . import (
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
    for module in reversed(modules):
        module.unregister()

if __name__ == "__main__":
    register()
