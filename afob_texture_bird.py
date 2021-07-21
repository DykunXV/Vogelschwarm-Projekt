import bpy
from bpy.types import Operator

class AFOB_OT_Texture_Bird_Op(Operator):
    bl_idname = "object.texture_bird"
    bl_label = "Texture bird"
    bl_description = "Gives the bird a texture."

    def execute(self, context):
        #needed for user input
        scene = context.scene
        mytool = scene.my_tool

        #switch shading type to see textures
        bpy.context.space_data.shading.type = 'MATERIAL'

        #select bird (bug prevention, in case of user doing something else, after generating the bird)
        bpy.ops.object.select_all(action='DESELECT')
        bpy.data.objects['AFOB_Bird'].select_set(True)
        bpy.context.view_layer.objects.active = bpy.data.objects['AFOB_Bird']

        #add material
        birdTexture = bpy.data.materials.new(name='AFOB_birdTexture')

        #add material to active object (bird)
        if bpy.context.object.material_slots:
            bpy.context.object.data.materials.clear()
        bpy.ops.object.material_slot_add()
        context.object.active_material = birdTexture

        #add setting for alpha channel
        bpy.context.object.active_material.blend_method = 'CLIP'
        bpy.context.object.active_material.shadow_method = 'CLIP'

        #add shade smooth
        bpy.ops.object.shade_smooth()
        
        #add image texture node depending on species chosen
        birdTexture.use_nodes = True
        nodes = birdTexture.node_tree.nodes
        shaderNode = nodes.new("ShaderNodeTexImage")    
        shaderNode.location = (-270, 300)
        if mytool.bird_species == 'OP1':
            shaderNode.image = bpy.data.images.load("//assets/AFOB_Original_birdDiffuse.png")
        if mytool.bird_species == 'OP2':
            shaderNode.image = bpy.data.images.load("//assets/AFOB_Black_Tern_birdDiffuse.png")
        if mytool.bird_species == 'OP3':
            shaderNode.image = bpy.data.images.load("//assets/AFOB_Bullfinch_birdDiffuse.png")

        #link image texture to principled bsdf
        principledBDSF = nodes.get('Principled BSDF')
        birdTexture.node_tree.links.new(shaderNode.outputs[0], principledBDSF.inputs[0])
        birdTexture.node_tree.links.new(shaderNode.outputs[1], principledBDSF.inputs[19])

        #select wings
        bpy.ops.object.select_all(action='DESELECT')
        bpy.data.objects['AFOB_Wings'].select_set(True)
        bpy.context.view_layer.objects.active = bpy.data.objects['AFOB_Wings']

        #add material
        wingsTexture = bpy.data.materials.new(name='AFOB_wingsTexture')

        #add material to active object (wings)
        if bpy.context.object.material_slots:
            bpy.context.object.data.materials.clear()
        bpy.ops.object.material_slot_add()
        context.object.active_material = wingsTexture

        #add setting for alpha channel
        bpy.context.object.active_material.blend_method = 'CLIP'
        bpy.context.object.active_material.shadow_method = 'CLIP'

        #add shade smooth
        bpy.ops.object.shade_smooth()
        
        #add image texture node 
        wingsTexture.use_nodes = True
        nodes = wingsTexture.node_tree.nodes
        shaderNode = nodes.new("ShaderNodeTexImage")    
        shaderNode.location = (-270, 300)
        if mytool.bird_species == 'OP1':
            shaderNode.image = bpy.data.images.load("//assets/AFOB_Original_wingsDiffuse.png")
        if mytool.bird_species == 'OP2':
            shaderNode.image = bpy.data.images.load("//assets/AFOB_Black_Tern_wingsDiffuse.png")
        if mytool.bird_species == 'OP3':
            shaderNode.image = bpy.data.images.load("//assets/AFOB_Bullfinch_wingsDiffuse.png")

        #link image texture to principled bsdf
        principledBDSF = nodes.get('Principled BSDF')
        wingsTexture.node_tree.links.new(shaderNode.outputs[0], principledBDSF.inputs[0])
        wingsTexture.node_tree.links.new(shaderNode.outputs[1], principledBDSF.inputs[19])

        return {'FINISHED'}