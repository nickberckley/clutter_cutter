import bpy
from ..constants import (
    PURGEABLE_TYPES,
    NON_PURGEABLE_TYPES,
)


typle = (PURGEABLE_TYPES + NON_PURGEABLE_TYPES)

#### ------------------------------ OPERATORS ------------------------------ ####

class FILE_OT_purge_by_name(bpy.types.Operator):
    bl_idname = "file.purge_by_name"
    bl_label = "Purge by Name"
    bl_description = "Purge data-blocks by name"
    bl_options = {'REGISTER', 'UNDO'}

    all: bpy.props.BoolProperty(
        name = "All Data Types",
        description = "Purge data-blocks of all types",
        default = False,
    )
    data_type: bpy.props.EnumProperty(
        name = "Data Type",
        items = NON_PURGEABLE_TYPES + PURGEABLE_TYPES,
        default = 'objects',
    )

    mode: bpy.props.EnumProperty(
        name = "Mode",
        items = [('INCLUDE', "Include", "Purge data-blocks that include string in their name"),
                 ('MATCH', "Match", "Purge data-blocks if entire name matches the string"),
                 ('STARTS', "Starts With", "Purge data-blocks if name starts with the string"),
                 ('ENDS', "Ends With", "Purge data-blocks if name ends with the string")],
        default = 'INCLUDE',
    )
    search_text: bpy.props.StringProperty(
        name = "Name",
    )
    unused_only: bpy.props.BoolProperty(
        name = "Unused Only",
        description = "Only purge orphaned data-blocks (with no users)",
        default = True,
    )

    def draw(self, context):
        layout = self.layout
        layout.use_property_split = True
        layout.use_property_decorate = False

        layout.prop(self, "all")
        if not self.all:
            layout.prop(self, "data_type")

        layout.prop(self, "mode")
        layout.prop(self, "search_text", text="Text", placeholder="String...")
        layout.prop(self, "unused_only")

    def invoke(self, context, event):
        return context.window_manager.invoke_props_dialog(self)

    def execute(self, context):
        if self.all:
            data_collection = [getattr(bpy.data, item[0]) for item in NON_PURGEABLE_TYPES + PURGEABLE_TYPES]
        else:
            data_collection = [getattr(bpy.data, self.data_type)]

        purged_count = 0
        for data_type in data_collection:
            for block in data_type:
                if block.name == "Viewer Node":
                    continue

                # Exclude used data-blocks if "Unused Only" chosen.
                if self.unused_only and block.users != 0:
                    continue

                if self.mode == 'INCLUDE' and self.search_text in block.name \
                or self.mode == 'MATCH' and self.search_text == block.name \
                or self.mode == 'STARTS' and block.name.startswith(self.search_text) \
                or self.mode == 'ENDS' and block.name.endswith(self.search_text):
                    data_type.remove(block)
                    purged_count += 1

        data_type_name = "data-blocks" if self.all else self.data_type.lower()
        if purged_count > 0:
            self.report({'INFO'}, f"Removed {purged_count} {data_type_name}")
        else:
            self.report({'INFO'}, f"No {data_type_name} match the criteria, 0 removed")
        return {'FINISHED'}



#### ------------------------------ REGISTRATION ------------------------------ ####

classes = (
    FILE_OT_purge_by_name,
)

def register():
    for cls in classes:
        bpy.utils.register_class(cls)

def unregister():
    for cls in reversed(classes):
        bpy.utils.unregister_class(cls)
