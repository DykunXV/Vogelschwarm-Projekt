from bpy.types import Panel

class AFOB_PT_Panel_Bird(Panel):
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_label = "Bird Parameters"
    bl_category = "AFOB Util"

    def draw(self, context):
        layout = self.layout

        row = layout.row()
        col = row.column()
        col.scale_y = 2.0
        col.operator("object.generate_bird", text="1. Generate bird")

class AFOB_PT_Panel_Texture(Panel):
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_label = "Texture Parameters"
    bl_category = "AFOB Util"

    def draw(self, context):
        layout = self.layout
        scene = context.scene
        mytool = scene.my_tool

        row = layout.row()
        col = row.column()
        col.prop(mytool, "bird_species")
        row = layout.row()
        col = row.column()
        col.scale_y = 2.0
        col.operator("object.texture_bird", text="2. Texture bird")

class AFOB_PT_Panel_Animation(Panel):
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_label = "Animation Parameters"
    bl_category = "AFOB Util"

    def draw(self, context):
        layout = self.layout
        scene = context.scene
        mytool = scene.my_tool

        row = layout.row()
        col = row.column()
        col.prop(mytool, "wingspan", slider=True)
        col.prop(mytool, "swing_speed", slider=True)
        col.prop(mytool, "resting_phase", slider=True)
        row = layout.row()
        col = row.column()
        col.scale_y = 2.0
        col.operator("object.animate_bird", text="3. Animate bird")


class AFOB_PT_Panel_Flock(Panel):
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_label = "Flock Parameters"
    bl_category = "AFOB Util"

    def draw(self, context):
        layout = self.layout
        scene = context.scene
        mytool = scene.my_tool

        row = layout.row()
        col = row.column()
        col.prop(mytool, "bird_size", slider=True)
        col.prop(mytool, "amount_of_birds")
        col.prop(mytool, "bird_spacing", slider=True)
        row = layout.row()
        col = row.column()
        col.scale_y = 2.0
        col.operator("object.multiply_bird", text="4. Multiply bird")