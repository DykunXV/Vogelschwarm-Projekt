import bpy

class AFOB_Properties(bpy.types.PropertyGroup):
    
    bird_species : bpy.props.EnumProperty(
        name= "Species",
        description= "Choose bird species",
        items= [('OP1', "Original", ""),
                ('OP2', "Black Tern", ""),
                ('OP3', "Bullfinch", "")
        ]
    )

    wingspan : bpy.props.FloatProperty(name= "Wingspan", default=2, min= 0.3, max= 4)

    swing_speed : bpy.props.FloatProperty(name= "Swing Speed Acceleration", default=1, min= 0.6, max= 2)

    resting_phase : bpy.props.FloatProperty(name= "Resting Phase Acceleration", default=1, min= 1, max= 3)

    bird_size : bpy.props.FloatProperty(name= "Bird Size", default=1, soft_min= 1, soft_max= 3)

    amount_of_birds : bpy.props.EnumProperty(
        name= "Amount of birds",
        description= "Choose amount of birds",
        items= [('OP1', "Few", ""),
                ('OP2', "Normal", ""),
                ('OP3', "Many", "") #for some reason choosing this option leads to a bug that some birds of the flock are missing their body and vice versa. a workaround would be joining body and wings, but that is not what im looking for
        ]
    )

    bird_spacing : bpy.props.FloatProperty(name= "Spacing of the birds", default=1, soft_min= 1, soft_max= 3)
    