import bpy

from bpy.types import Menu

from . import config


arrClasses = []

def prefix_name(opClass):
    opClass.__name__ = config.ADDON_PREFIX.upper() + '_MT_' + opClass.__name__
    arrClasses.append(opClass)
    return opClass

@prefix_name
class ContextMenu(Menu): 
    """Context Menu For Print Nodes"""
    # bl_idname = prefix_name(type(self).__name__)  #f'{config.ADDON_PREFIX.upper()}_MT_Main'
    bl_idname = "PRTND_MT_context_menu"
    bl_label = "PrintNodes"
    
    def draw(self, context):
        layout = self.layout
        layout.operator("prtnd.modal_ss_timer", text = "Take Screenshot Of Whole Tree", icon = "NODETREE")
        layout.operator("prtnd.modal_ss_timer", text = "Take Screenshot Of Selected Nodes", icon = "SELECT_SET").selection_only = True

# menu function(s)
def PrintNodes_menu_func(self, context):
    self.layout.menu("PRTND_MT_context_menu", icon="FCURVE_SNAPSHOT")

def register():
    for i in arrClasses:
        bpy.utils.register_class(i)
    
    bpy.types.NODE_MT_context_menu.append(PrintNodes_menu_func)


def unregister():
    for i in reversed(arrClasses):
        bpy.utils.unregister_class(i)

    bpy.types.NODE_MT_context_menu.remove(PrintNodes_menu_func)
