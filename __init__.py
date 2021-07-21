bl_info = {
    "name" : "Animated Flock Of Birds",
    "author" : "Dennis Fischer",
    "description" : "Generate a flock of animated birds.",
    "blender" : (2, 93, 1),
    "version" : (0, 0, 1),
    "location" : "View3D",
    "warning" : "",
    "category" : "Object"
}

import bpy

from . afob_properties import AFOB_Properties
from . afob_pnl import AFOB_PT_Panel_Bird, AFOB_PT_Panel_Texture, AFOB_PT_Panel_Animation, AFOB_PT_Panel_Flock
from . afob_generate_bird import AFOB_OT_Generate_Bird_Op
from . afob_texture_bird import AFOB_OT_Texture_Bird_Op
from . afob_animate_bird import AFOB_OT_Animate_Bird_Op
from . afob_multiply_bird import AFOB_OT_Multiply_Bird_Op

classes = (AFOB_Properties, AFOB_PT_Panel_Bird, AFOB_PT_Panel_Texture, AFOB_PT_Panel_Animation, AFOB_PT_Panel_Flock, AFOB_OT_Generate_Bird_Op, AFOB_OT_Texture_Bird_Op, AFOB_OT_Animate_Bird_Op, AFOB_OT_Multiply_Bird_Op)

def register():
    for c in classes:
        bpy.utils.register_class(c)
    bpy.types.Scene.my_tool = bpy.props.PointerProperty(type= AFOB_Properties)

def unregister():
    for c in classes:
        bpy.utils.unregister_class(c)
    del bpy.types.Scene.my_tool
