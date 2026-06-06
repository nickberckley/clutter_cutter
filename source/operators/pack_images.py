import bpy


#### ------------------------------ OPERATORS ------------------------------ ####

class FILE_OT_pack_image_by_name(bpy.types.Operator):
    bl_idname = "file.pack_image_by_name"
    bl_label = "Pack Images by Name"
    bl_options = {'REGISTER', 'UNDO'}

    keyword: bpy.props.StringProperty(name="Includes in Name")

    def invoke(self, context, event):
        wm = context.window_manager
        return wm.invoke_props_dialog(self)

    def execute(self, context):
        packed_count = 0
        for image in bpy.data.images:
            if self.keyword in image.name:
                image.pack()
                packed_count += 1

        self.report({'INFO'}, f"Packed {packed_count} images")
        return {'FINISHED'}


class FILE_OT_unpack_image_by_name(bpy.types.Operator):
    bl_idname = "file.unpack_image_by_name"
    bl_label = "Unpack Images by Name"
    bl_options = {'REGISTER', 'UNDO'}

    keyword: bpy.props.StringProperty(
        name = "Includes in Name",
    )
    unpack_method: bpy.props.EnumProperty(
        name = "Unpack Type",
        items=[('USE_LOCAL', 'Use file from current directory', ""),
               ('WRITE_LOCAL', 'Write file to current directory', ""),
               ('USE_ORIGINAL', 'Use file in original location', ""),
               ('WRITE_ORIGINAL', 'Write file to original location', "")],
        default = 'USE_LOCAL',
    )

    def execute(self, context):
        if not bpy.data.is_saved:
            self.report({'ERROR'}, ".blend file must be saved to unpack images")
            return {'CANCELLED'}

        unpacked_count = 0
        for image in bpy.data.images:
            if self.keyword in image.name:
                try:
                    image.unpack(method=self.unpack_method)
                    unpacked_count += 1
                except:
                    continue

        self.report({'INFO'}, f"Unpacked {unpacked_count} images")
        return {'FINISHED'}

    def invoke(self, context, event):
        wm = context.window_manager
        return wm.invoke_props_dialog(self)



#### ------------------------------ REGISTRATION ------------------------------ ####

classes = (
    FILE_OT_pack_image_by_name,
    FILE_OT_unpack_image_by_name,
)

def register():
    for cls in classes:
        bpy.utils.register_class(cls)

def unregister():
    for cls in reversed(classes):
        bpy.utils.unregister_class(cls)
