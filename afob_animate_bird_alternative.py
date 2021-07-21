## THIS IS THE NOW OUTDATED LOGIC I WOULD HAVE USED FOR EVERY BIRD TO HAVE A DIFFERENT ANIMATION, IF THIS WOULDNT LEAD TO A BUG WHICH I SADLY CANT FIX IN TIME

import bpy
from bpy.types import Operator

class AFOB_OT_Animate_Bird_Op(Operator):
    bl_idname = "object.animate_bird_alternative"
    bl_label = "Animate bird alternative"
    bl_description = "Animate bird alternative"

    amount_of_birds: int = 10 #TODO - this is the amount of birds with different animations. for the actual amount of birds, the ico-sphere has to be changed, as it is dependend of the number of vertices on the ico-sphere.
    animation_speed: float = 1
    animation_offset: int = 0

    def execute(self, context):
        #deform modifier
        bpy.ops.object.select_all(action='DESELECT')
        bpy.data.objects['Wings'].select_set(True)
        bpy.context.view_layer.objects.active = bpy.data.objects['Wings']
        bpy.ops.object.modifier_add(type='SIMPLE_DEFORM')
        bpy.context.object.modifiers["SimpleDeform"].deform_method = 'BEND'
        bpy.context.object.modifiers["SimpleDeform"].deform_axis = 'Y'
        bpy.context.object.modifiers["SimpleDeform"].origin = bpy.data.objects["Empty"]

        #select every object in the bird collection
        for obj in bpy.data.collections['Bird Collection'].all_objects:
            obj.select_set(True)

        #duplicate as long, until desired amount is reached
        i = 1
        while i < self.amount_of_birds:
            bpy.ops.object.duplicate_move(OBJECT_OT_duplicate={"linked":False, "mode":'TRANSLATION'}, TRANSFORM_OT_translate={"value":(0, 0, 0), "orient_type":'GLOBAL', "orient_matrix":((1, 0, 0), (0, 1, 0), (0, 0, 1)), "orient_matrix_type":'GLOBAL', "constraint_axis":(False, False, False), "mirror":True, "use_proportional_edit":False, "proportional_edit_falloff":'SMOOTH', "proportional_size":1, "use_proportional_connected":False, "use_proportional_projected":False, "snap":False, "snap_target":'CLOSEST', "snap_point":(0, 0, 0), "snap_align":False, "snap_normal":(0, 0, 0), "gpencil_strokes":False, "cursor_transform":False, "texture_space":False, "remove_on_cancel":False, "release_confirm":False, "use_accurate":False, "use_automerge_and_split":False})
            i += 1

        #set max keyframes
            bpy.context.scene.frame_end = 200
            bpy.context.scene.frame_start = 0

        #animate every bird with a offset of 10 frames
        for obj in bpy.data.objects:
            if "Wings" in obj.name:
                print(obj.name)
                bpy.ops.object.select_all(action='DESELECT')
                bpy.data.objects[obj.name].select_set(True)
                bpy.context.view_layer.objects.active = bpy.data.objects[obj.name]

                #define variable
                wings = bpy.data.objects[obj.name]

                #switch between wings up and down
                i = self.animation_offset 
                while i <= self.animation_offset + 100:
                    bpy.context.object.modifiers["SimpleDeform"].angle = 0.95
                    if i <= 200:
                        wings.modifiers['SimpleDeform'].keyframe_insert('angle', frame=i)
                    else:
                        wings.modifiers['SimpleDeform'].keyframe_insert('angle', frame=i - 200)
                        
                    bpy.context.object.modifiers["SimpleDeform"].angle = -0.95
                    if i + 10 <= 200:
                        wings.modifiers['SimpleDeform'].keyframe_insert('angle', frame=i + 10)
                    else:
                        wings.modifiers['SimpleDeform'].keyframe_insert('angle', frame=i + 10 - 200)
                    i += 20
                    
                #set start and ending keyframe
                bpy.context.object.modifiers["SimpleDeform"].angle = 0.2
                if 110 + self.animation_offset <= 200:
                    wings.modifiers['SimpleDeform'].keyframe_insert('angle', frame=110 + self.animation_offset)
                else:
                    wings.modifiers['SimpleDeform'].keyframe_insert('angle', frame=110 + self.animation_offset - 200)

                   
                bpy.context.object.modifiers["SimpleDeform"].angle = -0.2
                if 160 + self.animation_offset <= 200: 
                    wings.modifiers['SimpleDeform'].keyframe_insert('angle', frame=160 + self.animation_offset)
                else:
                    wings.modifiers['SimpleDeform'].keyframe_insert('angle', frame=160 + self.animation_offset - 200)

                bpy.context.object.modifiers["SimpleDeform"].angle = 0.2
                if 200 + self.animation_offset <= 200:
                    wings.modifiers['SimpleDeform'].keyframe_insert('angle', frame=200 + self.animation_offset)
                else:
                    wings.modifiers['SimpleDeform'].keyframe_insert('angle', frame=200 + self.animation_offset - 200)

            self.animation_offset += 10
        

        return {'FINISHED'}

