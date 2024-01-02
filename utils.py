import bpy
import os


def makeDirectory():  # Manage Directory for saving screenshots

    if bpy.data.filepath and bpy.context.preferences.addons[__package__].preferences.force_secondary_dir == False:
        # save image in the place where the blendfile is saved, in a newly created subfolder (if saved and force_default_directory is set to false)
        Directory = os.path.join(os.path.split(
            bpy.data.filepath)[0], 'NodesShots')

        if os.path.isdir(Directory) == False:
            os.mkdir(Directory)

    else:
        # just use the secondary directory otherwise
        Directory = bpy.context.preferences.addons[__package__].preferences.secondary_save_dir

    return Directory


# function to display popup message on command
def printNodesPopUp(message="", title="PrintNodes PopUp", icon=""):

    def draw(self, context):
        self.layout.label(text=message)

    bpy.context.window_manager.popup_menu(draw, title=title, icon=icon)


def select_nodes(nodes, select=True):
    for current_node in nodes:
        current_node.select = select


def find_min_max_coords(nodes) -> tuple[float]:
    '''find the min and max coordinates of given nodes.
    Returns: Xmin, Ymin, Xmax, Ymax'''
    Xmin: float
    Xmax: float
    Ymin: float
    Ymax: float

    (x, y) = nodes[0].location
    (w, h) = nodes[0].dimensions

    Xmin = x
    Xmax = x + w
    Ymin = y - h
    Ymax = y

    for node in nodes:
        (x, y) = node.location
        (w, h) = node.dimensions

        Xmin = min(Xmin, x)
        Xmax = max(Xmax, x + w)
        Ymin = min(Ymin, y - h)
        Ymax = max(Ymax, y)

    return Xmin, Ymin, Xmax, Ymax
