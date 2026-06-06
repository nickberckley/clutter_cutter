import bpy
from ..functions import purge_orphans


#### ------------------------------ OPERATORS ------------------------------ ####

class OUTLINER_OT_purge_by_type(bpy.types.Operator):
    bl_idname = "outliner.purge"
    bl_label = "Purge Orphaned Data"
    bl_description = "Removes all unused (userless) blocks from .blend file for a given data-type"
    bl_options = {'REGISTER', 'UNDO'}

    data_type: bpy.props.StringProperty(
    )
    recursive: bpy.props.BoolProperty(
        name = "Recursive",
        default = False,
    )

    def invoke(self, context, event):
        self.recursive = event.shift
        return self.execute(context)

    def execute(self, context):
        purged_count, recursive_count = purge_orphans(self.data_type, recursive=self.recursive)

        if self.recursive:
            self.report({'INFO'}, f"Purged {purged_count} orphaned {self.data_type} (and {recursive_count} recursive)")
        else:
            self.report({'INFO'}, f"Purged {purged_count} orphaned {self.data_type}")
        return {'FINISHED'}



#### ------------------------------ REGISTRATION ------------------------------ ####

classes = (
    OUTLINER_OT_purge_by_type,
)

def register():
    for cls in classes:
        bpy.utils.register_class(cls)

def unregister():
    for cls in reversed(classes):
        bpy.utils.unregister_class(cls)
