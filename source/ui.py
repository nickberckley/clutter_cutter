import bpy
from .constants import PURGEABLE_TYPES
from .functions import orphaned_counter


#### ------------------------------ MENUS ------------------------------ ####

class OUTLINER_MT_purge_by_type(bpy.types.Menu):
    bl_idname = 'OUTLINER_MT_purge_by_type'
    bl_label = 'Purge Orphans'
    bl_description = 'Completely remove userless data by type'

    def draw(self, context):
        layout = self.layout
        layout.operator_context = 'INVOKE_DEFAULT'
        col = layout.column(align=True)
        grid = col.grid_flow(row_major=False, columns=3, even_columns=True, even_rows=True)

        col_size = 9
        first_col  = PURGEABLE_TYPES[0:col_size]
        second_col = PURGEABLE_TYPES[col_size:col_size*2]
        third_col  = PURGEABLE_TYPES[col_size*2:col_size*3]

        for (identifier, name, __, icon, __) in first_col + second_col + third_col:
            row = grid.row()
            count = orphaned_counter(identifier)
            text = name + " (" + str(count) + ")"
            row.operator("outliner.purge", text=text, icon=icon).data_type=identifier
            if count < 1:
                row.enabled = False



#### ------------------------------ /menu_appendages/ ------------------------------ ####

def outliner_purge_button(self, context):
    layout = self.layout
    op = layout.operator("wm.call_menu", text="", icon='ORPHAN_DATA')
    op.name = "OUTLINER_MT_purge_by_type"


def file_cleanup_menu(self, context):
    layout = self.layout
    layout.operator("file.purge_by_name", text="Purge by Name...")


def pack_image_menu(self, context):
    layout = self.layout
    layout.separator()
    layout.operator("file.pack_image_by_name")
    layout.operator("file.unpack_image_by_name")



#### ------------------------------ REGISTRATION ------------------------------ ####

classes = [
    OUTLINER_MT_purge_by_type,
]

def register():
    for cls in classes:
        bpy.utils.register_class(cls)

    # MENU
    bpy.types.OUTLINER_HT_header.append(outliner_purge_button)
    bpy.types.TOPBAR_MT_file_cleanup.append(file_cleanup_menu)
    bpy.types.TOPBAR_MT_file_external_data.append(pack_image_menu)


def unregister():
    for cls in reversed(classes):
        bpy.utils.unregister_class(cls)

    # MENU
    bpy.types.OUTLINER_HT_header.remove(outliner_purge_button)
    bpy.types.TOPBAR_MT_file_cleanup.remove(file_cleanup_menu)
    bpy.types.TOPBAR_MT_file_external_data.remove(pack_image_menu)
