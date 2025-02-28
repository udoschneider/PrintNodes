# PrintNodes addon for Blender 2.80+ to take high quality screenshots of node trees
# Managed by: Binit (aka Yeetus)

# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful, but
# WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTIBILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU
# General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program. If not, see <http://www.gnu.org/licenses/>.

from . import utils
from . import settings
from . import config
from . import image
import importlib


from . import install
from . import menu
from . import ops
from . import preferences

importlib.reload(install)
importlib.reload(menu)
importlib.reload(ops)
importlib.reload(preferences)

# The following import are only to enforce reload during development
importlib.reload(image)
importlib.reload(config)
importlib.reload(settings)
importlib.reload(utils)


bl_info = {
    "name": "PrintNodes",
    "author": "Binit",
    "description": "Takes high quality screenshot of a node tree",
    "blender": (3, 1, 0),
    "version": (1, 2, 0),
    "location": "Node Editor > Context Menu (Right Click)",
    "warning": "",
    "category": "Node"
}


def register():
    install.addPackages()
    preferences.register()
    ops.register()
    menu.register()


def unregister():
    preferences.unregister()
    ops.unregister()
    menu.unregister()
