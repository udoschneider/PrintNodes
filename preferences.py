import bpy
from bpy.types import AddonPreferences
from bpy.props import StringProperty, BoolProperty, IntProperty, FloatVectorProperty

from . import config

arrClasses = []

def prefix_name(opClass):
    opClass.__name__ = config.ADDON_PREFIX.upper() + '_' + opClass.__name__
    arrClasses.append(opClass)
    return opClass

@prefix_name
class Preferences(AddonPreferences): # setting up perferences
    bl_idname = __package__

    secondary_save_dir: StringProperty(
        name = "Secondary Directory",
        subtype = 'DIR_PATH',
        default = bpy.context.preferences.filepaths.temporary_directory,
        )

    force_secondary_dir: BoolProperty(
        name = "Always Use Secondary Directory",
        default = False,
        )

    padding_amount: IntProperty(
        name = "Padding Amount (in px)",
        default = 30,
        )

    node_outline_color: FloatVectorProperty(
        name="Node Outline Color",
        description="Set this to outline of a node in non active/selected state.",
        size=3,
        subtype='COLOR',
        default=[0.0,0.0,0.0],
        soft_max=1.0,
        soft_min=0.0,
    )

    disable_auto_crop: BoolProperty(
        name = 'Disable Auto Cropping',
        description = 'Check this if something is not working properly',
        default = False,
        )

    def draw(self, context):
        layout = self.layout
        layout.label(text = "A subfolder in the same directory as the blend file will be used to save the images.")
        layout.label(text = "Unless the file is unsaved or 'Always Use Secondary Directory' is checked.")
        layout.label(text = "In which case, the Secondary Directory will be used")
        layout.prop(self, "secondary_save_dir")
        layout.prop(self, "force_secondary_dir")
        layout.separator()
        layout.prop(self, "node_outline_color")
        layout.separator()
        layout.prop(self, "padding_amount")
        layout.prop(self, "disable_auto_crop")


def register():
    for i in arrClasses:
        bpy.utils.register_class(i)


def unregister():
    for i in reversed(arrClasses):
        bpy.utils.unregister_class(i)