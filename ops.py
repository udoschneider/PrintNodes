import bpy
import os

from bpy.types import Operator
from bpy.props import BoolProperty

from . import utils
from . import config
from . import image
from . import settings


arrClasses = []


def prefix_name(opClass):
    opClass.__name__ = config.ADDON_PREFIX.upper() + '_OT_' + opClass.__name__
    arrClasses.append(opClass)
    return opClass


@prefix_name
# modal operator to take parts of the whole shot every at every set interval, while not interrupting the rest of blender's functioning (for the most part)
class ModalScreenshotTimer(Operator):
    """Take screenshot of active node tree. Press RightClick or Esc to cancel during process."""
    bl_idname = "prtnd.modal_ss_timer"
    bl_label = "Take Tree Screenshot"

    settings: settings.Settings
    selection_only: BoolProperty(default=False)

    _timer: bpy.types.Timer = None
    Xmin = Ymin = Xmax = Ymax = 0
    ix = iy = 0
    forced_cancel: bool = False

    def modal(self, context, event):
        context.window.cursor_set("STOP")
        if event.type in {'RIGHTMOUSE', 'ESC'}:  # force cancel
            self.forced_cancel = True
            self.cancel(context)
            return {'CANCELLED'}

        if event.type == 'TIMER':
            tree = context.space_data.edit_tree
            margin = bpy.context.preferences.addons[__package__].preferences.safety_margin_amount
            view = context.region.view2d
            area = bpy.context.area
            dx = area.width - 2 * margin
            dy = area.height - 2 * margin

            path = os.path.join(utils.makeDirectory(),
                                f'Prt_y{self.iy}_x{self.ix}.png')
            # take screenshot of current view as a 'tile' to be further stitched and processed
            bpy.ops.screen.screenshot_area(filepath=path)

            # check if already at the other corner of the tree, if yes, sucessfully terminate
            if tree.view_center[1] > self.Ymax and tree.view_center[0] > self.Xmax:
                self.cancel(context)
                return {'CANCELLED'}

            # if exceeded rightmost edge, pan all the way back to leftmost edge and pan y up once to prepare for the next 'layer' of tiles
            if tree.view_center[0] > self.Xmax:
                bpy.ops.view2d.pan(deltax=-(self.ix*dx), deltay=dy)
                self.ix = 0
                self.iy += 1

            # just pan to the right if no other condition applies (i.e. we're somewhere in the middle of the tile strip)
            else:
                bpy.ops.view2d.pan(deltax=dx, deltay=0)
                self.ix += 1

        return {'PASS_THROUGH'}  # pass for next iteration

    def execute(self, context):
        context.window.cursor_set("STOP")
        self.settings = settings.Settings()
        self.settings.store(context)
        self.settings.set_for_screenshot(context)

        if self.selection_only:
            # perform within the selected nodes only
            nodes = [node for node in context.selected_nodes if node.parent == None]
        else:
            # perform within the whole tree
            nodes = [
                node for node in context.space_data.edit_tree.nodes if node.parent == None]

        zoom = bpy.context.preferences.addons[__package__].preferences.zoom_delta
        bpy.ops.view2d.reset()
        bpy.ops.view2d.zoom(deltax=zoom, deltay=zoom)

        self.Xmin, self.Ymin, self.Xmax, self.Ymax = utils.find_min_max_coords(
            nodes)

        xPan, yPan = context.region.view2d.view_to_region(
            self.Xmin, self.Ymin, clip=False)
        margin = bpy.context.preferences.addons[__package__].preferences.safety_margin_amount
        bpy.ops.view2d.pan(deltax=xPan-margin * 2, deltay=yPan-margin * 2)

        # Selecting nodes to avoid the noodle dimming.
        utils.select_nodes(nodes, select=True)
        wm = context.window_manager
        # add timer to begin with, for the `modal` process
        self._timer = wm.event_timer_add(0.02, window=context.window)
        wm.modal_handler_add(self)

        return {'RUNNING_MODAL'}

    def cancel(self, context):
        if self.forced_cancel:
            utils.printNodesPopUp(
                message="Process Force Cancelled", icon="CANCEL")

        else:
            area = bpy.context.area
            margin = bpy.context.preferences.addons[__package__].preferences.safety_margin_amount
            # being the stitching and processing process of the tiles
            image.stitchTiles(self.ix + 1, self.iy + 1, margin)
            utils.printNodesPopUp(
                message="Screenshot Saved Successfully", icon="CHECKMARK")

        # revert all the temporary settings back to original
        self.settings.restore(context)
        bpy.ops.node.view_all()

        wm = context.window_manager
        wm.event_timer_remove(self._timer)
        context.window.cursor_set("DEFAULT")


def register():
    for i in arrClasses:
        bpy.utils.register_class(i)


def unregister():
    for i in arrClasses:
        bpy.utils.unregister_class(i)
