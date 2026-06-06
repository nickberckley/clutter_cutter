import bpy
from ..functions import purge_unrecursive


#### ------------------------------ OPERATORS ------------------------------ ####

class OUTLINER_OT_purge_by_type(bpy.types.Operator):
    bl_idname = "outliner.purge"
    bl_label = "Purge Orphaned Data"
    bl_description = "Removes all unused (userless) blocks from .blend file for a given data-type"
    bl_options = {'REGISTER', 'UNDO'}

    data_type: bpy.props.StringProperty(
    )

    def execute(self, context):
        purged_count = purge_unrecursive(self.data_type)

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
