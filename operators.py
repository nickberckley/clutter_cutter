import bpy
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


class FILE_OT_purge_orphaned_by_name(bpy.types.Operator):
    bl_idname = "outliner.purge_orphaned_data_by_name"
    bl_label = "Purge Orphaned Data by Name"
    bl_description = "Purge orphaned data by name and data type"
    bl_options = {'REGISTER', 'UNDO'}

    search_text: bpy.props.StringProperty(name="Name")
    data_type: bpy.props.EnumProperty(
        items=[
            ('IMAGES', 'Image', '', 'IMAGE_DATA', 1),
            ('MATERIALS', 'Mateiral', '', 'MATERIAL_DATA', 2),
            ('NODE_GROUPS', 'Node Group', '', 'NODETREE', 3),
            ('WORLDS', 'World', '', 'WORLD_DATA', 4),
            ('BRUSHES', 'Brush', '', 'BRUSH_DATA', 5),
            ('TEXTURES', 'Texture', '', 'TEXTURE_DATA', 6),
            ('PALETTES', 'Palette', '', 'COLOR', 7),
            ('LINESTYLES', 'Line Style', '', 'LINE_DATA', 8),
            ('PARTICLES', 'Particle', '', 'PARTICLE_DATA', 9),
            ('MESHES', 'Mesh', '', 'MESH_DATA', 10),
            ('CURVES', 'Curve', '', 'CURVE_DATA', 11),
            ('GREASE_PENCILS', 'Grease Pencil', '', 'GREASEPENCIL', 12),
            ('METABALLS', 'Metaball', '', 'META_DATA', 13),
            ('HAIR_CURVES', 'Hair', '', 'CURVES_DATA', 14),
            ('VOLUMES', 'Volume', '', 'VOLUME_DATA', 15),
            ('LATTICES', 'Lattice', '', 'LATTICE_DATA', 16),
            ('SPEAKERS', 'Speaker', '', 'OUTLINER_DATA_SPEAKER', 17),
            ('LIGHTPROBES', 'Light Probe', '', 'OUTLINER_DATA_LIGHTPROBE', 18),
            ('ACTIONS', 'Action', '', 'ACTION', 19),
            ('ARMATURES', 'Armature', '', 'ARMATURE_DATA', 20),
#            ('SHAPE_KEYS', 'Shape Keys', '', 'SHAPEKEY_DATA', 21),
            ('CAMERAS', 'Camera', '', 'CAMERA_DATA', 21),
            ('LIGHTS', 'Lights', '', 'LIGHT_DATA', 22),
            ('MOVIECLIPS', 'Movie Clip', '', 'TRACKER', 23),
            ('SOUNDS', 'Sound', '', 'SOUND', 24),
            ('TEXTS', 'Text', '', 'TEXT', 25),
            ('FONT', 'Font', '', 'FONT_DATA', 26),
        ],
        name="Data Type",
        default='IMAGES',
    )

    def draw(self, context):
        layout = self.layout
        layout.use_property_split = True
        layout.use_property_decorate = False
        layout.prop(self, "data_type", text="in Data Type:")
        layout.prop(self, "search_text", text="Includes:")


    def invoke(self, context, event):
        return context.window_manager.invoke_props_dialog(self)

    def execute(self, context):
        data_collection = None
        if self.data_type == 'IMAGES':
            data_collection = bpy.data.images
        elif self.data_type == 'MATERIALS':
            data_collection = bpy.data.materials
        elif self.data_type == 'NODE_GROUPS':
            data_collection = bpy.data.node_groups
        elif self.data_type == 'WORLDS':
            data_collection = bpy.data.worlds
        elif self.data_type == 'BRUSHES':
            data_collection = bpy.data.brushes
        elif self.data_type == 'TEXTURES':
            data_collection = bpy.data.textures
        elif self.data_type == 'PALETTES':
            data_collection = bpy.data.palettes
        elif self.data_type == 'LINESTYLES':
            data_collection = bpy.data.linestyles
        elif self.data_type == 'PARTICLES':
            data_collection = bpy.data.particles
        elif self.data_type == 'MESHES':
            data_collection = bpy.data.meshes
        elif self.data_type == 'CURVES':
            data_collection = bpy.data.curves
        elif self.data_type == 'GREASE_PENCILS':
            data_collection = bpy.data.grease_pencils
        elif self.data_type == 'METABALLS':
            data_collection = bpy.data.metaballs
        elif self.data_type == 'HAIR_CURVES':
            data_collection = bpy.data.hair_curves
        elif self.data_type == 'VOLUMES':
            data_collection = bpy.data.volumes
        elif self.data_type == 'LATTICES':
            data_collection = bpy.data.lattices
        elif self.data_type == 'SPEAKERS':
            data_collection = bpy.data.speakers
        elif self.data_type == 'LIGHTPROBES':
            data_collection = bpy.data.lightprobes
        elif self.data_type == 'ACTIONS':
            data_collection = bpy.data.actions
        elif self.data_type == 'ARMATURES':
            data_collection = bpy.data.armatures
#        elif self.data_type == 'SHAPE_KEYS':
#            data_collection = bpy.data.shape_keys
        elif self.data_type == 'CAMERAS':
            data_collection = bpy.data.cameras
        elif self.data_type == 'LIGHTS':
            data_collection = bpy.data.lights
        elif self.data_type == 'MOVIECLIPS':
            data_collection = bpy.data.movieclips
        elif self.data_type == 'SOUNDS':
            data_collection = bpy.data.sounds
        elif self.data_type == 'TEXTS':
            data_collection = bpy.data.texts
        elif self.data_type == 'FONT':
            data_collection = bpy.data.fonts

        if data_collection is not None:
            purged_count = 0
            for block in data_collection:
                if block.users == 0 and self.search_text in block.name:
                    data_collection.remove(block)
                    purged_count += 1

        if purged_count > 0:
            self.report({'INFO'}, f"Removed {purged_count} {self.data_type.lower()} containing '{self.search_text}'")
        else:
            self.report({'INFO'}, f"No orphaned {self.data_type.lower()} containing '{self.search_text}' found")
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
#            bpy.data.shape_keys,
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

    keyword: bpy.props.StringProperty(name="Includes in Name")
    unpack_method: bpy.props.EnumProperty(
        items=[
            ('USE_LOCAL', 'Use file from current directory', '', '', 0),
            ('WRITE_LOCAL', 'Write file to current directory', '', '', 1),
            ('USE_ORIGINAL', 'Use file in original location', '', '', 2),
            ('WRITE_ORIGINAL', 'Write file to original location', '', '', 3),
        ],
        name="Unpack Type",
        default='USE_LOCAL',
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

    FILE_OT_purge_orphaned_by_name,
    FILE_OT_purge_orphaned_duplicates,
    FILE_OT_pack_image_by_name,
    FILE_OT_unpack_image_by_name,
]

def register():
    for cls in classes :
        bpy.utils.register_class(cls)

def unregister():
    for cls in reversed(classes) :
        bpy.utils.unregister_class(cls)
