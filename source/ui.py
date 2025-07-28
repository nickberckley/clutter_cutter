import bpy
from .functions import orphaned_counter


#### ------------------------------ PANELS ------------------------------ ####

class OUTLINER_MT_purge_by_type(bpy.types.Menu):
    bl_idname = 'OUTLINER_MT_purge_by_type'
    bl_label = 'Purge Orphans'
    bl_description = 'Purge orphaned data by data type'
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'WINDOW'

    def draw(self, context):
        layout = self.layout
        layout.operator_context = 'INVOKE_DEFAULT'
        col = layout.column(align=True)
        grid = col.grid_flow(row_major=False, columns=3, even_columns=True, even_rows=True)

        """
        NOTE: Cache files, paint curves, shape keys can be userless, but there is no way of removing them individually from Blender.
        NOTE: Masks have a bug that always keeps at least one user on them, so even if they're userless it's impossible to detect that.
        """

        # First Column
        first_col = (
            ('images', "Image", 'IMAGE_DATA'),
            ('materials', "Material", 'MATERIAL_DATA'),
            ('node_groups', "Node Group", 'NODETREE'),
            ('worlds', "World", 'WORLD_DATA'),
            ('brushes', "Brush", 'BRUSH_DATA'),
            ('textures', "Texture", 'TEXTURE_DATA'),
            ('palettes', "Palette", 'COLOR'),
            ('linestyles', "Line Style", 'LINE_DATA'),
            ('particles', "Particles", 'PARTICLE_DATA'),
        )

        second_col = (
            ('meshes', "Mesh", 'MESH_DATA'),
            ('curves', "Curve", 'CURVE_DATA'),
            ('grease_pencils', "Grease Pencil", 'GREASEPENCIL'),
            ('metaballs', "Metaball", 'META_DATA'),
            ('hair_curves', "Hair", 'OUTLINER_DATA_CURVES'),
            ('pointclouds', "Point Cloud", 'POINTCLOUD_DATA'),
            ('volumes', "Volume", 'OUTLINER_DATA_VOLUME'),
            ('lattices', "Lattice", 'LATTICE_DATA'),
            ('speakers', "Speaker", 'OUTLINER_DATA_SPEAKER'),
        )

        third_col = (
            ('actions', "Action", 'ACTION'),
            ('armatures', "Armature", 'ARMATURE_DATA'),
            ('cameras', "Camera", 'CAMERA_DATA'),
            ('lights', "Light", 'LIGHT_DATA'),
            ('lightprobes', "Light Probe", 'OUTLINER_DATA_LIGHTPROBE'),
            ('movieclips', "Movie Clip", 'TRACKER'),
            ('sounds', "Sound", 'FILE_SOUND'),
            ('texts', "Text", 'TEXT'),
            ('fonts', "Font", 'FONT_DATA'),
        )

        for (identifier, name, icon) in first_col + second_col + third_col:
            row = grid.row()
            count = orphaned_counter(identifier)
            row.operator("outliner.purge", text=name + " (" + str(count) + ")", icon=icon).data_type=identifier
            if count < 1:
                row.enabled = False



#### ------------------------------ MENUS ------------------------------ ####

def purge_button(self, context):
    layout = self.layout
    layout.operator("wm.call_menu", text="", icon='ORPHAN_DATA').name = "OUTLINER_MT_purge_by_type"


def deep_clean_menu(self, context):
    layout = self.layout
    layout.operator("file.purge_by_name")


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
    bpy.types.OUTLINER_HT_header.append(purge_button)
    bpy.types.TOPBAR_MT_file_cleanup.append(deep_clean_menu)
    bpy.types.TOPBAR_MT_file_external_data.append(pack_image_menu)


def unregister():
    for cls in reversed(classes):
        bpy.utils.unregister_class(cls)

    # MENU
    bpy.types.OUTLINER_HT_header.remove(purge_button)
    bpy.types.TOPBAR_MT_file_cleanup.remove(deep_clean_menu)
    bpy.types.TOPBAR_MT_file_external_data.remove(pack_image_menu)
