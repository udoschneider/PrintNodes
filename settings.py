import bpy


class Settings:
    grid_level: int = 0
    scroll_color: tuple
    wire_select_color: tuple
    node_selected: tuple
    node_active: tuple
    header: bool
    ui: bool
    overlay: bool

    def store(self, context):
        theme = context.preferences.themes[0]
        space_data = context.space_data

        self.grid_level = theme.node_editor.grid_levels
        self.scroll_color = tuple(theme.user_interface.wcol_scroll.item)
        self.wire_select_color = tuple(theme.node_editor.wire_select)
        self.node_selected = tuple(theme.node_editor.node_selected)
        self.node_active = tuple(theme.node_editor.node_active)

        self.header = space_data.show_region_header
        self.toolbar = space_data.show_region_toolbar
        self.ui = space_data.show_region_ui
        self.overlay = space_data.overlay.show_context_path

    def restore(self, context):
        theme = context.preferences.themes[0]
        space_data = context.space_data

        theme.node_editor.grid_levels = self.grid_level
        theme.user_interface.wcol_scroll.item = self.scroll_color
        theme.node_editor.wire_select = self.wire_select_color
        theme.node_editor.node_selected = self.node_selected
        theme.node_editor.node_active = self.node_active

        space_data.show_region_header = self.header
        space_data.show_region_ui = self.ui
        space_data.overlay.show_context_path = self.overlay

    def set_for_screenshot(self, context):
        theme = context.preferences.themes[0]
        pref = bpy.context.preferences.addons[__package__].preferences
        space_data = context.space_data

        # turn gridlines off, trimming empty space doesn't work otherwise
        theme.node_editor.grid_levels = 0
        theme.user_interface.wcol_scroll.item = (0, 0, 0, 0)
        theme.node_editor.wire_select = (0, 0, 0, 0)
        theme.node_editor.node_selected = pref.node_outline_color
        theme.node_editor.node_active = pref.node_outline_color

        space_data.overlay.show_context_path = False
        space_data.show_region_header = False
        space_data.show_region_ui = False
