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
    for module in reversed(modules):
        module.unregister()

if __name__ == "__main__":
    register()
