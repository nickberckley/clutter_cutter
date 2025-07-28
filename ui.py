import bpy
from .functions import orphaned_counter


#### ------------------------------ /panels/ ------------------------------ ####

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

        # First Row
        top1 = grid.row()
        imagecount = orphaned_counter('images')
        top1.operator('outliner.purge', text='Image' + ' (' + str(imagecount) + ')', icon='IMAGE_DATA').data_type="images"
        if imagecount < 1:
            top1.enabled = False

        top2 = grid.row()
        materialcount = orphaned_counter('materials')
        top2.operator('outliner.purge', text='Material' + ' (' + str(materialcount) + ')', icon='MATERIAL_DATA').data_type="materials"
        if materialcount < 1:
            top2.enabled = False

        top3 = grid.row()
        nodegroupcount = orphaned_counter('node_groups')
        top3.operator('outliner.purge', text='Node Group' + ' (' + str(nodegroupcount) + ')', icon='NODETREE').data_type="node_groups"
        if nodegroupcount < 1:
            top3.enabled = False

        top4 = grid.row()
        worldcount = orphaned_counter('worlds')
        top4.operator('outliner.purge', text='World' + ' (' + str(worldcount) + ')', icon='WORLD_DATA').data_type="worlds"
        if worldcount < 1:
            top4.enabled = False

        top5 = grid.row()
        brushcount = orphaned_counter('brushes')
        top5.operator('outliner.purge', text='Brush' + ' (' + str(brushcount) + ')', icon='BRUSH_DATA').data_type="brushes"
        if brushcount < 1:
            top5.enabled = False

        top6 = grid.row()
        texturecount = orphaned_counter('textures')
        top6.operator('outliner.purge', text='Texture' + ' (' + str(texturecount) + ')', icon='TEXTURE_DATA').data_type="textures"
        if texturecount < 1:
            top6.enabled = False

        top7 = grid.row()
        palettecount = orphaned_counter('palettes')
        top7.operator('outliner.purge', text='Palette' + ' (' + str(palettecount) + ')', icon='COLOR').data_type="palettes"
        if palettecount < 1:
            top7.enabled = False

        top8 = grid.row()
        linestylecount = orphaned_counter('linestyles')
        top8.operator('outliner.purge', text='Line Style' + ' (' + str(linestylecount) + ')', icon='LINE_DATA').data_type="linestyles"
        if linestylecount < 1:
            top8.enabled = False

        top9 = grid.row()
        particlecount = orphaned_counter('particles')
        top9.operator('outliner.purge', text='Particles' + ' (' + str(particlecount) + ')', icon='PARTICLE_DATA').data_type="particles"
        if particlecount < 1:
            top9.enabled = False


        # Second Row
        mid1 = grid.row()
        meshcount = orphaned_counter('meshes')
        mid1.operator('outliner.purge', text='Mesh' + ' (' + str(meshcount) + ')', icon='MESH_DATA').data_type="meshes"
        if meshcount < 1:
            mid1.enabled = False

        mid2 = grid.row()
        curvecount = orphaned_counter('curves')
        mid2.operator('outliner.purge', text='Curve' + ' (' + str(curvecount) + ')', icon='CURVE_DATA').data_type="curves"
        if curvecount < 1:
            mid2.enabled = False

        mid3 = grid.row()
        greasepencilcount = orphaned_counter('grease_pencils')
        mid3.operator('outliner.purge', text='Grease Pencil' + ' (' + str(greasepencilcount) + ')', icon='GREASEPENCIL').data_type="grease_pencils"
        if greasepencilcount < 1:
            mid3.enabled = False

        mid4 = grid.row()
        metaballcount = orphaned_counter('metaballs')
        mid4.operator('outliner.purge', text='Metaball' + ' (' + str(metaballcount) + ')', icon='META_DATA').data_type="metaballs"
        if metaballcount < 1:
            mid4.enabled = False

        mid5 = grid.row()
        haircount = orphaned_counter('hair_curves')
        mid5.operator('outliner.purge', text='Hair' + ' (' + str(haircount) + ')', icon='OUTLINER_DATA_CURVES').data_type="hair_curves"
        if haircount < 1:
            mid5.enabled = False

        mid6 = grid.row()
        volumecount = orphaned_counter('volumes')
        mid6.operator('outliner.purge', text='Volume' + ' (' + str(volumecount) + ')', icon='OUTLINER_DATA_VOLUME').data_type="volumes"
        if volumecount < 1:
            mid6.enabled = False

        mid7 = grid.row()
        latticecount = orphaned_counter('lattices')
        op = mid7.operator('outliner.purge', text='Lattice' + ' (' + str(latticecount) + ')', icon='LATTICE_DATA').data_type="lattices"
        if latticecount < 1:
            mid7.enabled = False

        mid8 = grid.row()
        speakercount = orphaned_counter('speakers')
        op = mid8.operator('outliner.purge', text='Speaker' + ' (' + str(speakercount) + ')', icon='OUTLINER_DATA_SPEAKER').data_type="speakers"
        if speakercount < 1:
            mid8.enabled = False

        mid9 = grid.row()
        lightprobecount = orphaned_counter('lightprobes')
        op = mid9.operator('outliner.purge', text='Light Probe' + ' (' + str(lightprobecount) + ')', icon='OUTLINER_DATA_LIGHTPROBE').data_type="lightprobes"
        if lightprobecount < 1:
            mid9.enabled = False


        # Third Row
        bot1 = grid.row()
        actioncount = orphaned_counter('actions')
        bot1.operator('outliner.purge', text='Action' + ' (' + str(actioncount) + ')', icon='ACTION').data_type="actions"
        if actioncount < 1:
            bot1.enabled = False

        bot2 = grid.row()
        armaturecount = orphaned_counter('armatures')
        bot2.operator('outliner.purge', text='Armature' + ' (' + str(armaturecount) + ')', icon='ARMATURE_DATA').data_type="armatures"
        if armaturecount < 1:
            bot2.enabled = False

#        bot3 = grid.row()
#        shapekeycount = orphaned_counter('shape_keys')
#        bot3.operator('outliner.purge', text='Shape Keys' + ' (' + str(shapekeycount) + ')', icon='SHAPEKEY_DATA').data_type="shapekeys"
#        if shapekeycount < 1:
#            bot3.enabled = False

        bot4 = grid.row()
        cameracount = orphaned_counter('cameras')
        bot4.operator('outliner.purge', text='Camera' + ' (' + str(cameracount) + ')', icon='CAMERA_DATA').data_type="cameras"
        if cameracount < 1:
            bot4.enabled = False

        bot5 = grid.row()
        lightcount = orphaned_counter('lights')
        bot5.operator('outliner.purge', text='Light' + ' (' + str(lightcount) + ')', icon='LIGHT_DATA').data_type="lights"
        if lightcount < 1:
            bot5.enabled = False

        bot6 = grid.row()
        movieclipcount = orphaned_counter('movieclips')
        bot6.operator('outliner.purge', text='Movie Clip' + ' (' + str(movieclipcount) + ')', icon='TRACKER').data_type="movieclips"
        if movieclipcount < 1:
            bot6.enabled = False

        bot7 = grid.row()
        soundcount = orphaned_counter('sounds')
        bot7.operator('outliner.purge', text='Sound' + ' (' + str(soundcount) + ')', icon='FILE_SOUND').data_type="sounds"
        if soundcount < 1:
            bot7.enabled = False

        bot8 = grid.row()
        textcount = orphaned_counter('texts')
        bot8.operator('outliner.purge', text='Text' + ' (' + str(textcount) + ')', icon='TEXT').data_type="texts"
        if textcount < 1:
            bot8.enabled = False

        bot9 = grid.row()
        fontcount = orphaned_counter('fonts')
        bot9.operator('outliner.purge', text='Font' + ' (' + str(fontcount) + ')', icon='FONT_DATA').data_type="fonts"
        if fontcount < 1:
            bot9.enabled = False



#### ------------------------------ /menus/ ------------------------------ ####

def purge_button(self, context):
    layout = self.layout
    layout.operator("wm.call_menu", text="", icon="ORPHAN_DATA").name = "OUTLINER_MT_purge_by_type"


def deep_clean_menu(self, context):
    layout = self.layout
    layout.separator()
    layout.operator("outliner.purge_orphaned_data_by_name")
    layout.operator("outliner.purge_orphaned_data_duplicates")


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
    for cls in classes :
        bpy.utils.register_class(cls)

    bpy.types.OUTLINER_HT_header.append(purge_button)
    bpy.types.TOPBAR_MT_file_cleanup.append(deep_clean_menu)
    bpy.types.TOPBAR_MT_file_external_data.append(pack_image_menu)

def unregister():
    for cls in reversed(classes) :
        bpy.utils.unregister_class(cls)

    bpy.types.OUTLINER_HT_header.remove(purge_button)
    bpy.types.TOPBAR_MT_file_cleanup.remove(deep_clean_menu)
    bpy.types.TOPBAR_MT_file_external_data.remove(pack_image_menu)
