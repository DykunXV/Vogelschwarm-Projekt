import bpy
from bpy.types import Operator

class AFOB_OT_Animate_Bird_Op(Operator):
    bl_idname = "object.animate_bird"
    bl_label = "Animate bird"
    bl_description = "Animate bird"
    
    starting_frame = 1
    ending_frame = 200

    def execute(self, context):
        scene = context.scene
        mytool = scene.my_tool

        #bug prevention, if user wishes to change parameters
        if bpy.data.objects['AFOB_Wings'].modifiers:
            bpy.data.objects['AFOB_Wings'].modifiers.remove(bpy.data.objects['AFOB_Wings'].modifiers.get("SimpleDeform"))
        bpy.data.objects['AFOB_Wings'].animation_data_clear()

        #deform modifier
        bpy.ops.object.select_all(action='DESELECT')
        bpy.data.objects['AFOB_Wings'].select_set(True)
        bpy.context.view_layer.objects.active = bpy.data.objects['AFOB_Wings']
        bpy.ops.object.modifier_add(type='SIMPLE_DEFORM')
        bpy.context.object.modifiers["SimpleDeform"].deform_method = 'BEND'
        bpy.context.object.modifiers["SimpleDeform"].deform_axis = 'Y'
        bpy.context.object.modifiers["SimpleDeform"].origin = bpy.data.objects["AFOB_Empty"]
        print(bpy.data.objects['AFOB_Wings'].modifiers.get("SimpleDeform"))

        #set max keyframes
        bpy.context.scene.frame_start = self.starting_frame
        bpy.context.scene.frame_end = self.ending_frame

        #set start and ending keyframe
        wings = bpy.data.objects['AFOB_Wings']
        bpy.context.object.modifiers["SimpleDeform"].angle = 0.2
        wings.modifiers['SimpleDeform'].keyframe_insert('angle', frame=self.starting_frame) 
        bpy.context.object.modifiers["SimpleDeform"].angle = -0.2    
        wings.modifiers['SimpleDeform'].keyframe_insert('angle', frame=self.ending_frame/4*(1/mytool.resting_phase))
        bpy.context.object.modifiers["SimpleDeform"].angle = 0.2
        wings.modifiers['SimpleDeform'].keyframe_insert('angle', frame=(self.ending_frame/2)*(1/mytool.resting_phase))
        bpy.context.object.modifiers["SimpleDeform"].angle = 0.2
        wings.modifiers['SimpleDeform'].keyframe_insert('angle', frame=self.ending_frame)

        #switch between wings up and down
        i = self.ending_frame/2*(1/mytool.resting_phase)+10
        while i <= self.ending_frame-20:
            bpy.context.object.modifiers["SimpleDeform"].angle = mytool.wingspan
            wings.modifiers['SimpleDeform'].keyframe_insert('angle', frame=i)
            bpy.context.object.modifiers["SimpleDeform"].angle = -mytool.wingspan
            wings.modifiers['SimpleDeform'].keyframe_insert('angle', frame=i + 10*(1/mytool.swing_speed))
            i += 20*(1/mytool.swing_speed)
        
        return {'FINISHED'}