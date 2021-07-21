import bpy
from bpy.types import Operator

class AFOB_OT_Generate_Bird_Op(Operator):
    bl_idname = "object.generate_bird"
    bl_label = "Generate bird"
    bl_description = "Generate a bird."

    #these values were supposed to be changable in the panel, but this would have created problems with the textures, as the textures are not dynamically created.
    bird_length: float = 2
    bird_width: float = 1
    bird_height: float = 0.8

    def execute(self, context):
        #generate collection and set active
        collection = bpy.data.collections.new('AFOB Bird Collection')
        bpy.context.scene.collection.children.link(collection)
        layer_collection = bpy.context.view_layer.layer_collection.children[collection.name]
        bpy.context.view_layer.active_layer_collection = layer_collection
        
        #add the starting cube
        bpy.ops.mesh.primitive_cube_add(
            location=(0, 0, 0),
            size=1,
            scale=(self.bird_length, self.bird_width, self.bird_height)
        )
        
        #add subdivision and apply it    
        bpy.ops.object.subdivision_set(level=1, relative=False)
        bpy.ops.object.modifier_apply(modifier="Subdivision")

        #define variables
        context = bpy.context
        ob = context.object
        me = ob.data

        #give the cube a name
        ob.name = 'AFOB_Bird'
        me.name = 'AFOB_Birdmesh'
        
        #add a function to clear the current selection and call it
        def clear_selection():
            for g in me.vertices[:] + me.edges[:] + me.polygons[:]:
                g.select = False         
        clear_selection()
        
        #change selection to vertices, because otherwise it will cause problems    
        bpy.ops.object.editmode_toggle()    
        bpy.ops.mesh.select_mode(use_extend=False, use_expand=False, type='VERT')
        bpy.ops.object.editmode_toggle()

        #add bevel to selected vertices
        me.vertices[12].select = True
        me.vertices[13].select = True
        me.vertices[18].select = True
        me.vertices[19].select = True
        me.vertices[21].select = True
        me.vertices[23].select = True
        me.vertices[24].select = True
        me.vertices[25].select = True
        bpy.ops.object.mode_set(mode='EDIT')
        bpy.ops.mesh.select_mode(use_extend=False, use_expand=False, type='VERT')
        bpy.ops.mesh.bevel(offset_type='PERCENT', offset=0, offset_pct=30, segments=2, release_confirm=True)
        bpy.ops.object.mode_set(mode='OBJECT')
        clear_selection()
        
        #resize the beak    
        me.polygons[0].select = True
        me.polygons[1].select = True
        me.polygons[2].select = True
        me.polygons[3].select = True
        bpy.ops.object.editmode_toggle()
        bpy.context.scene.tool_settings.use_proportional_edit = True
        bpy.ops.transform.resize(value=(0.25, 0.25, 0.25), orient_type='GLOBAL', orient_matrix=((1, 0, 0), (0, 1, 0), (0, 0, 1)), orient_matrix_type='GLOBAL', mirror=True, use_proportional_edit=True, proportional_edit_falloff='SPHERE', proportional_size=0.217629, use_proportional_connected=False, use_proportional_projected=False)
        bpy.context.scene.tool_settings.use_proportional_edit = False
        bpy.ops.object.editmode_toggle()
        clear_selection()
        
        #extrude tail and resize it
        me.edges[20].select = True
        me.edges[22].select = True
        bpy.ops.object.editmode_toggle()
        bpy.ops.mesh.extrude_context_move(MESH_OT_extrude_context={"use_normal_flip":False, "use_dissolve_ortho_edges":False, "mirror":False}, TRANSFORM_OT_translate={"value":(0.4, 0, 0), "orient_type":'GLOBAL', "orient_matrix":((1, 0, 0), (0, 1, 0), (0, 0, 1)), "orient_matrix_type":'GLOBAL', "constraint_axis":(True, True, True), "mirror":False, "use_proportional_edit":False, "proportional_edit_falloff":'SMOOTH', "proportional_size":0.77, "use_proportional_connected":False, "use_proportional_projected":False, "snap":False, "snap_target":'CLOSEST', "snap_point":(0, 0, 0), "snap_align":False, "snap_normal":(0, 0, 0), "gpencil_strokes":False, "cursor_transform":False, "texture_space":False, "remove_on_cancel":False, "release_confirm":True, "use_accurate":False, "use_automerge_and_split":False})
        bpy.ops.transform.resize(value=(1.5, 1.5, 1.5), orient_type='GLOBAL', orient_matrix=((1, 0, 0), (0, 1, 0), (0, 0, 1)), orient_matrix_type='GLOBAL', mirror=True, use_proportional_edit=False, proportional_edit_falloff='SPHERE', proportional_size=0.826446, use_proportional_connected=False, use_proportional_projected=False)
        bpy.ops.object.editmode_toggle()
        clear_selection()
            
        #change tail heights    
        me.edges[82].select = True
        bpy.ops.object.editmode_toggle()
        bpy.ops.transform.translate(value=(0, 0, 0.025), orient_type='GLOBAL', orient_matrix=((1, 0, 0), (0, 1, 0), (0, 0, 1)), orient_matrix_type='GLOBAL', constraint_axis=(True, True, True), mirror=True, use_proportional_edit=False, proportional_edit_falloff='SPHERE', proportional_size=0.826446, use_proportional_connected=False, use_proportional_projected=False, release_confirm=True)
        bpy.ops.object.editmode_toggle()
        clear_selection()
        me.vertices[42].select = True
        me.vertices[43].select = True
        bpy.ops.object.editmode_toggle()
        bpy.ops.transform.translate(value=(0, 0, -0.025), orient_type='GLOBAL', orient_matrix=((1, 0, 0), (0, 1, 0), (0, 0, 1)), orient_matrix_type='GLOBAL', constraint_axis=(True, True, True), mirror=True, use_proportional_edit=False, proportional_edit_falloff='SPHERE', proportional_size=0.826446, use_proportional_connected=False, use_proportional_projected=False, release_confirm=True)
        bpy.ops.object.editmode_toggle()
        
        #add wings and name them
        bpy.ops.mesh.primitive_cube_add(size=0.25, enter_editmode=False, align='WORLD', location=(self.bird_length/10, 0, 0), scale=(self.bird_length, self.bird_width*16, self.bird_height/4))
        context = bpy.context
        ob = context.object
        me = ob.data
        ob.name = 'AFOB_Wings'
        me.name = 'AFOB_Wingsmesh'
        
        #loop cut and slide
        bpy.ops.object.editmode_toggle()
        bpy.ops.mesh.loopcut_slide(MESH_OT_loopcut={"number_cuts":10, "smoothness":0, "falloff":'INVERSE_SQUARE', "object_index":0, "edge_index":8, "mesh_select_mode_init":(True, False, False)}, TRANSFORM_OT_edge_slide={"value":-0, "single_side":False, "use_even":False, "flipped":False, "use_clamp":True, "mirror":True, "snap":False, "snap_target":'CLOSEST', "snap_point":(0, 0, 0), "snap_align":False, "snap_normal":(0, 0, 0), "correct_uv":True, "release_confirm":False, "use_accurate":False})
        bpy.ops.mesh.loopcut_slide(MESH_OT_loopcut={"number_cuts":1, "smoothness":0, "falloff":'INVERSE_SQUARE', "object_index":0, "edge_index":61, "mesh_select_mode_init":(True, False, False)}, TRANSFORM_OT_edge_slide={"value":0, "single_side":False, "use_even":False, "flipped":False, "use_clamp":True, "mirror":True, "snap":False, "snap_target":'CLOSEST', "snap_point":(0, 0, 0), "snap_align":False, "snap_normal":(0, 0, 0), "correct_uv":True, "release_confirm":False, "use_accurate":False})
        bpy.ops.object.editmode_toggle()

        #make wings look like wings
        clear_selection()
        me.polygons[2].select = True
        me.polygons[26].select = True
        bpy.ops.object.editmode_toggle()
        bpy.ops.transform.resize(value=(1, 1.11614, 1), orient_type='GLOBAL', orient_matrix=((1, 0, 0), (0, 1, 0), (0, 0, 1)), orient_matrix_type='GLOBAL', constraint_axis=(False, True, False), mirror=True, use_proportional_edit=False, proportional_edit_falloff='SMOOTH', proportional_size=1, use_proportional_connected=False, use_proportional_projected=False, release_confirm=True)
        bpy.ops.object.editmode_toggle()
        clear_selection()
        me.polygons[0].select = True
        me.polygons[36].select = True
        bpy.ops.object.editmode_toggle()
        bpy.ops.transform.resize(value=(1, 0.813468, 1), orient_type='GLOBAL', orient_matrix=((1, 0, 0), (0, 1, 0), (0, 0, 1)), orient_matrix_type='GLOBAL', constraint_axis=(False, True, False), mirror=True, use_proportional_edit=False, proportional_edit_falloff='SMOOTH', proportional_size=1, use_proportional_connected=False, use_proportional_projected=False, release_confirm=True)
        bpy.ops.object.editmode_toggle()
        clear_selection()
        me.polygons[28].select = True
        me.polygons[34].select = True
        me.polygons[37].select = True
        me.polygons[38].select = True
        me.polygons[44].select = True
        me.polygons[45].select = True
        bpy.ops.object.editmode_toggle()
        bpy.ops.transform.resize(value=(1.32772, 1, 1), orient_type='GLOBAL', orient_matrix=((1, 0, 0), (0, 1, 0), (0, 0, 1)), orient_matrix_type='GLOBAL', constraint_axis=(True, False, False), mirror=True, use_proportional_edit=False, proportional_edit_falloff='SMOOTH', proportional_size=1, use_proportional_connected=False, use_proportional_projected=False, release_confirm=True)
        bpy.ops.object.editmode_toggle()
            
        #add empty for incoming deform
        bpy.ops.object.empty_add(type='PLAIN_AXES', align='WORLD', location=(0, 0, 0), scale=(1, 1, 1))
        bpy.context.object.name = 'AFOB_Empty'
        bpy.ops.transform.rotate(value=1.5708, orient_axis='Z', orient_type='GLOBAL', orient_matrix=((1, 0, 0), (0, 1, 0), (0, 0, 1)), orient_matrix_type='GLOBAL', constraint_axis=(False, False, True), mirror=True, use_proportional_edit=False, proportional_edit_falloff='SMOOTH', proportional_size=1, use_proportional_connected=False, use_proportional_projected=False, release_confirm=True)
        bpy.ops.transform.rotate(value=1.5708, orient_axis='X', orient_type='GLOBAL', orient_matrix=((1, 0, 0), (0, 1, 0), (0, 0, 1)), orient_matrix_type='GLOBAL', constraint_axis=(True, False, False), mirror=True, use_proportional_edit=False, proportional_edit_falloff='SMOOTH', proportional_size=1, use_proportional_connected=False, use_proportional_projected=False, release_confirm=True)
        
        #make wings child object
        bpy.ops.object.select_all(action='DESELECT')
        bpy.data.objects['AFOB_Bird'].select_set(True)
        bpy.data.objects['AFOB_Wings'].select_set(True)
        bpy.data.objects['AFOB_Empty'].select_set(True)
        bpy.context.view_layer.objects.active = bpy.data.objects['AFOB_Bird']
        bpy.ops.object.parent_set()

        #set wings origin to geometry
        bpy.ops.object.select_all(action='DESELECT')
        bpy.data.objects['AFOB_Wings'].select_set(True)
        bpy.ops.object.origin_set(type='ORIGIN_GEOMETRY', center='MEDIAN')

        #mark seems for wings and unwrap
        clear_selection()
        me.edges[2].select = True
        me.edges[5].select = True
        me.edges[8].select = True
        me.edges[11].select = True
        i = 22
        while i <= 31:
            me.edges[i].select = True
            i += 1
        i = 42
        while i <= 51:
            me.edges[i].select = True
            i += 1
        me.edges[93].select = True
        me.edges[95].select = True
        bpy.context.view_layer.objects.active = bpy.data.objects['AFOB_Wings']
        bpy.ops.object.editmode_toggle()
        bpy.ops.mesh.mark_seam(clear=False)
        bpy.ops.mesh.select_all(action='SELECT')
        bpy.ops.uv.unwrap(method='ANGLE_BASED', margin=0.001)
        bpy.ops.uv.select_all(action='SELECT')
        bpy.ops.uv.pack_islands(margin=0.1)
        bpy.ops.object.editmode_toggle()

        #mark seems for bird and unwrap
        clear_selection()
        bpy.ops.object.select_all(action='DESELECT')
        bpy.data.objects['AFOB_Bird'].select_set(True)
        bpy.context.view_layer.objects.active = bpy.data.objects['AFOB_Bird']
        bpy.context.object.data.edges[17].select = True
        bpy.context.object.data.edges[21].select = True
        bpy.context.object.data.edges[57].select = True
        bpy.context.object.data.edges[59].select = True
        bpy.context.object.data.edges[71].select = True
        bpy.context.object.data.edges[73].select = True
        bpy.context.object.data.edges[82].select = True
        bpy.ops.object.editmode_toggle()
        bpy.ops.mesh.mark_seam(clear=False)
        bpy.ops.mesh.select_all(action='SELECT')
        bpy.ops.uv.unwrap(method='ANGLE_BASED', margin=0.001)
        bpy.ops.uv.select_all(action='SELECT')
        bpy.ops.uv.pack_islands(margin=0.1)
        bpy.ops.object.editmode_toggle()

        #Recalculate inverted normal
        clear_selection()
        bpy.context.object.data.polygons[40].select = True
        bpy.ops.object.editmode_toggle()
        bpy.ops.mesh.normals_make_consistent(inside=False)
        bpy.ops.object.editmode_toggle()

        return {'FINISHED'}