import bpy
import itertools
from .functions import purge_unrecursive


#### ------------------------------ OPERATORS ------------------------------ ####

class OUTLINER_OT_purge(bpy.types.Operator):
    bl_idname = "outliner.purge"
    bl_label = "Purge Orphaned Data"
    bl_description = "Removes all unused (userless) blocks from .blend file for given data-type"
    bl_options = {'REGISTER', 'UNDO'}

    data_type: bpy.props.StringProperty(
    )

    def execute(self, context):
        purged_count = purge_unrecursive(self.data_type)

        self.report({'INFO'}, f"Purged {purged_count} orphaned {self.data_type}")
        return {'FINISHED'}


class FILE_OT_purge_by_name(bpy.types.Operator):
    bl_idname = "file.purge_by_name"
    bl_label = "Purge by Name..."
    bl_description = "Purge data-blocks by name"
    bl_options = {'REGISTER', 'UNDO'}

    search_text: bpy.props.StringProperty(
        name = "Name",
    )
    mode: bpy.props.EnumProperty(
        name = "Mode",
        items = [('INCLUDE', "Include", "Purge data-blocks that include string in their name"),
                 ('MATCH', "Match", "Purge data-blocks if entire name matches the string"),
                 ('STARTS', "Starts With", "Purge data-blocks if name starts with the string"),
                 ('ENDS', "Ends With", "Purge data-blocks if name ends with the string")],
        default = 'INCLUDE',
    )
    all: bpy.props.BoolProperty(
        name = "All Data Types",
        description = "Purge data-blocks of all types",
        default = False,
    )
    data_type: bpy.props.EnumProperty(
        name = "Data Type",
        items = [('images', "Image", "", 'IMAGE_DATA', 1),
                 ('materials', "Mateiral", "", 'MATERIAL_DATA', 2),
                 ('node_groups', "Node Group", "", 'NODETREE', 3),
                 ('worlds', "World", "", 'WORLD_DATA', 4),
                 ('brushes', "Brush", "", 'BRUSH_DATA', 5),
                 ('textures', "Texture", "", 'TEXTURE_DATA', 6),
                 ('palettes', "Palette", "", 'COLOR', 7),
                 ('linestyles', "Line Style", "", 'LINE_DATA', 8),
                 ('particles', "Particle", "", 'PARTICLE_DATA', 9),
                 ('meshes', "Mesh", "", 'MESH_DATA', 10),
                 ('curves', "Curve", "", 'CURVE_DATA', 11),
                 ('grease_pencils', "Grease Pencil", "", 'GREASEPENCIL', 12),
                 ('metaballs', "Metaball", "", 'META_DATA', 13),
                 ('hair_curves', "Hair", "", 'CURVES_DATA', 14),
                 ('pointclouds', "Point Cloud", "", 'POINTCLOUD_DATA', 15),
                 ('volumes', "Volume", "", 'VOLUME_DATA', 16),
                 ('lattices', "Lattice", "", 'LATTICE_DATA', 17),
                 ('speakers', "Speaker", "", 'OUTLINER_DATA_SPEAKER', 18),
                 ('actions', "Action", "", 'ACTION', 19),
                 ('armatures', "Armature", "", 'ARMATURE_DATA', 20),
                 ('cameras', "Camera", "", 'CAMERA_DATA', 21),
                 ('lights', "Lights", "", 'LIGHT_DATA', 22),
                 ('lightprobes', "Light Probe", "", 'OUTLINER_DATA_LIGHTPROBE', 23),
                 ('movieclips', "Movie Clip", "", 'TRACKER', 24),
                 ('sounds', "Sound", "", 'SOUND', 25),
                 ('texts', "Text", "", 'TEXT', 26),
                 ('fonts', "Font", "", 'FONT_DATA', 27)],
        default = 'images',
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
            types = ["images", "materials", "node_groups", "worlds", "brushes", "textures", "palettes", "linestyles", "particles",
                     "meshes", "curves", "grease_pencils", "metaballs", "hair_curves", "pointclouds", "volumes", "lattices", "speakers",
                     "actions", "armatures", "cameras", "lights", "lightprobes", "movieclips", "sounds", "texts", "fonts"]
            data_collection = []
            for type in types:
                data_collection.append(getattr(bpy.data, type))
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

        if purged_count > 0:
            data_type_name = "data-blocks" if self.all else self.data_type.lower()
            self.report({'INFO'}, f"Removed {purged_count} {data_type_name}")
        else:
            self.report({'INFO'}, f"No {self.data_type.lower()} match criteria")
        return {'FINISHED'}


class FILE_OT_purge_orphaned_duplicates(bpy.types.Operator):
    bl_idname = "outliner.purge_orphaned_data_duplicates"
    bl_label = "Purge Orphaned Duplicates"
    bl_description = "Purge orphaned duplicates in all data types"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        data_collections = [
            bpy.data.images,
            bpy.data.materials,
            bpy.data.node_groups,
            bpy.data.worlds,
            bpy.data.particles,
            bpy.data.brushes,
            bpy.data.textures,
            bpy.data.palettes,
            bpy.data.linestyles,
            bpy.data.meshes,
            bpy.data.curves,
            bpy.data.grease_pencils,
            bpy.data.metaballs,
            bpy.data.hair_curves,
            bpy.data.lattices,
            bpy.data.volumes,
            bpy.data.speakers,
            bpy.data.lightprobes,
            bpy.data.actions,
            bpy.data.armatures,
            bpy.data.cameras,
            bpy.data.lights,
            bpy.data.movieclips,
            bpy.data.sounds,
            bpy.data.texts,
            bpy.data.fonts,
        ]

        purged_count = 0
        for data_collection in data_collections:
            for block in data_collection:
                if block.users == 0 and '.0' in block.name:
                    data_collection.remove(block)
                    purged_count += 1

        self.report({'INFO'}, "Purged {} orphaned duplicates".format(purged_count))
        return {'FINISHED'}


class FILE_OT_pack_image_by_name(bpy.types.Operator):
    bl_idname = "file.pack_image_by_name"
    bl_label = "Pack Images by Name"
    bl_description = "Pack images if they include keyword in their name, for example: Brick_Wall; Roughness; and etc."
    bl_options = {'REGISTER', 'UNDO'}

    keyword: bpy.props.StringProperty(name="Includes in Name")

    def execute(self, context):
        packed_count = 0
        for image in bpy.data.images:
            if self.keyword in image.name:
                image.pack()
                packed_count += 1

        self.report({'INFO'}, "Packed {} images that include {} in the name".format(packed_count, self.keyword))
        return {'FINISHED'}

    def invoke(self, context, event):
        wm = context.window_manager
        return wm.invoke_props_dialog(self)


class FILE_OT_unpack_image_by_name(bpy.types.Operator):
    bl_idname = "file.unpack_image_by_name"
    bl_label = "Unpack Images by Name"
    bl_description = "Unpack images if they include keyword in their name, for example: Brick_Wall; Roughness; and etc."
    bl_options = {'REGISTER', 'UNDO'}

    keyword: bpy.props.StringProperty(
        name = "Includes in Name",
    )
    unpack_method: bpy.props.EnumProperty(
        items=[('USE_LOCAL', 'Use file from current directory', ""),
               ('WRITE_LOCAL', 'Write file to current directory', ""),
               ('USE_ORIGINAL', 'Use file in original location', ""),
               ('WRITE_ORIGINAL', 'Write file to original location', "")],
        name = "Unpack Type",
        default = 'USE_LOCAL',
    )

    def execute(self, context):
        if not bpy.data.is_saved:
            self.report({'ERROR'}, ".blend file must be saved to unpack images")
            return {'CANCELLED'}

        unpacked_count = 0
        for image in bpy.data.images:
            if self.keyword in image.name:
                if self.unpack_method == "USE_LOCAL":
                    image.unpack(method="USE_LOCAL")
                    unpacked_count += 1
                elif self.unpack_method == "WRITE_LOCAL":
                    image.unpack(method="WRITE_LOCAL")
                    unpacked_count += 1
                elif self.unpack_method == "USE_ORIGINAL":
                    image.unpack(method="USE_ORIGINAL")
                    unpacked_count += 1
                elif self.unpack_method == "WRITE_ORIGINAL":
                    image.unpack(method="WRITE_ORIGINAL")
                    unpacked_count += 1

        self.report({'INFO'}, "Unpacked {} images that include {} in the name".format(unpacked_count, self.keyword))
        return {'FINISHED'}

    def invoke(self, context, event):
        wm = context.window_manager
        return wm.invoke_props_dialog(self)



#### ------------------------------ REGISTRATION ------------------------------ ####

classes = [
    OUTLINER_OT_purge,
    FILE_OT_purge_by_name,
    FILE_OT_purge_orphaned_duplicates,
    FILE_OT_pack_image_by_name,
    FILE_OT_unpack_image_by_name,
]

def register():
    for cls in classes:
        bpy.utils.register_class(cls)

def unregister():
    for cls in reversed(classes):
        bpy.utils.unregister_class(cls)
