import bpy
from bpy.types import Operator

class AFOB_OT_Multiply_Bird_Op(Operator):
    bl_idname = "object.multiply_bird"
    bl_label = "Multiply bird"
    bl_description = "Multiply the bird to create a flock."

    def execute(self, context):
        #needed for user input
        scene = context.scene
        mytool = scene.my_tool

        #bug prevention, if user wishes to change parameters
        if bpy.data.collections.get('AFOB Particles'):
            bpy.data.collections.remove(bpy.data.collections.get('AFOB Particles'))
        
        #select every object in the bird collection and hide it
        bpy.ops.object.select_all(action='DESELECT')
        for obj in bpy.data.collections['AFOB Bird Collection'].all_objects:
            obj.select_set(True)
        bpy.ops.object.hide_view_set(unselected=False)

        #generate collection and set active
        collection = bpy.data.collections.new('AFOB Particles')
        bpy.context.scene.collection.children.link(collection)
        layer_collection = bpy.context.view_layer.layer_collection.children[collection.name]
        bpy.context.view_layer.active_layer_collection = layer_collection

        #add ico-sphere and apply displace modifier with created texture
        if mytool.amount_of_birds == 'OP1':
            bpy.ops.mesh.primitive_ico_sphere_add(subdivisions = 1, radius=mytool.bird_spacing, enter_editmode=False, align='WORLD', location=(0, 0, 0), scale=(1, 1, 1))
        if mytool.amount_of_birds == 'OP2':
            bpy.ops.mesh.primitive_ico_sphere_add(subdivisions = 2, radius=mytool.bird_spacing, enter_editmode=False, align='WORLD', location=(0, 0, 0), scale=(1, 1, 1))
        if mytool.amount_of_birds == 'OP3':
            bpy.ops.mesh.primitive_ico_sphere_add(subdivisions = 3, radius=mytool.bird_spacing, enter_editmode=False, align='WORLD', location=(0, 0, 0), scale=(1, 1, 1))
        bpy.context.object.name = 'AFOB_Icosphere'
        bpy.ops.transform.resize(value=(1.2, 1.7, 1), orient_type='GLOBAL', orient_matrix=((1, 0, 0), (0, 1, 0), (0, 0, 1)), orient_matrix_type='GLOBAL', constraint_axis=(True, True, True), mirror=True, use_proportional_edit=False, proportional_edit_falloff='SMOOTH', proportional_size=1, use_proportional_connected=False, use_proportional_projected=False)
        bpy.data.textures.new("AFOB Bird Movement", 'CLOUDS')
        modifier = bpy.data.objects['AFOB_Icosphere'].modifiers.new(name="Displace", type='DISPLACE')
        bpy.context.object.modifiers["Displace"].texture_coords = 'OBJECT'
        bpy.context.object.modifiers["Displace"].strength = 1.8
        modifier.texture = bpy.data.textures['AFOB Bird Movement']
        modifier.texture.noise_scale = 0.7
        modifier.texture.noise_depth = 0

        #add keyframes for ico-sphere (flock)
        flock  = bpy.data.objects['AFOB_Icosphere']
        flock.keyframe_insert(data_path="location", frame=1)
        flock.location = (-10, 0, 0)
        flock.keyframe_insert(data_path="location", frame=100)
        flock.location = (-20, 0, 0)
        flock.keyframe_insert(data_path="location", frame=200)

        #move flock back to start for incoming child object
        flock.location = (0, 0, 0)

        #add empty sphere and make it child
        bpy.ops.object.empty_add(type='SPHERE', align='WORLD', location=(0, 0, 0), scale=(1, 1, 1))
        bpy.context.object.name = 'AFOB_Empty_Ico'
        bpy.ops.object.select_all(action='DESELECT')
        bpy.data.objects['AFOB_Icosphere'].select_set(True)
        bpy.data.objects['AFOB_Empty_Ico'].select_set(True)
        bpy.context.view_layer.objects.active = bpy.data.objects['AFOB_Icosphere']
        bpy.ops.object.parent_set()

        #add keyframe data for empty
        empty = bpy.data.objects['AFOB_Empty_Ico']
        empty.keyframe_insert(data_path="location", frame=1)
        empty.location = (0, -0.5*mytool.bird_spacing, 0)
        empty.keyframe_insert(data_path="location", frame=100)
        empty.location = (0, 0, 0)
        empty.keyframe_insert(data_path="location", frame=200)

        #add empty as object to displace modifier
        bpy.ops.object.select_all(action='DESELECT')
        bpy.data.objects['AFOB_Icosphere'].select_set(True)
        bpy.context.object.modifiers["Displace"].texture_coords_object = bpy.data.objects["AFOB_Empty_Ico"]

        #add particle system and change settings
        object = bpy.context.object
        object.modifiers.new(name='AFOB_Particle_System',type='PARTICLE_SYSTEM').name
        bpy.context.object.particle_systems['AFOB_Particle_System'].settings.name = 'AFOB_ParticleSettings'
        bpy.data.particles['AFOB_ParticleSettings'].frame_end = 1
        bpy.data.particles['AFOB_ParticleSettings'].physics_type = 'NO'
        bpy.data.particles['AFOB_ParticleSettings'].lifetime = 200
        bpy.data.particles['AFOB_ParticleSettings'].render_type = 'COLLECTION'
        bpy.data.particles['AFOB_ParticleSettings'].instance_collection = bpy.data.collections["AFOB Bird Collection"]
        bpy.data.particles['AFOB_ParticleSettings'].use_collection_count = True
        bpy.data.particles['AFOB_ParticleSettings'].use_rotations = True
        bpy.data.particles['AFOB_ParticleSettings'].rotation_mode = 'GLOB_Y'
        bpy.data.particles['AFOB_ParticleSettings'].particle_size = mytool.bird_size/10 #the /10 is just for the number in the panel to look nicer
        bpy.data.particles['AFOB_ParticleSettings'].emit_from = 'VERT'
        bpy.context.object.show_instancer_for_render = False
        bpy.context.object.show_instancer_for_viewport = False

        return {'FINISHED'}