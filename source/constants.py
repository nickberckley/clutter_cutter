
PURGEABLE_TYPES = [
    ('images', "Image", "", 'IMAGE_DATA', 1),
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
    ('fonts', "Font", "", 'FONT_DATA', 27),
]

NON_PURGEABLE_TYPES = [
    ('objects', "Object", "", 'OBJECT_DATAMODE', 28),
    ('collections', "Collection", "", 'OUTLINER_COLLECTION', 29),
    ('scenes', "Scene", "", 'SCENE_DATA', 30),
]


# `bpy.data.cache_files`, `bpy.data.paint_curves`, `bpy.data.shape_keys`
# can be userless, but there is no way of removing them individually from Blender.

# `bpy.data.masks` have a bug that always keeps at least one user on them,
# so even if they're userless it's impossible to detect that.

# Leftover `bpy.data` items, not worthy of covering:
# - annotations
# - libraries
# - screens
# - window_managers
# - workspaces

# Also members of `bpy.data`, but unrelated types:
# - colorspace
# - filepath
# - is_dirty
# - is_saved
# - use_autopack
# - version
