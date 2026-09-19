# menu_overlay.py
#
# Copyright 2026 Muqtadir
#
# SPDX-License-Identifier: GPL-3.0-or-later

import gi

gi.require_version("Gtk", "4.0")
gi.require_version("Adw", "1")

from gi.repository import Adw, GObject, Gtk

from slipspace.components.menu.menu_item import MenuItem

GObject.type_ensure(MenuItem)


@Gtk.Template(resource_path="/com/muqtxdir/slipspace/components/menu/menu-overlay.ui")
class MenuOverlay(Adw.Bin):
    __gtype_name__ = "MenuOverlay"

    _split_view: Adw.OverlaySplitView = Gtk.Template.Child("split_view")
    _items: Adw.Sidebar = Gtk.Template.Child("items")
    _power: Adw.Sidebar = Gtk.Template.Child("power")

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self._power.props.selected = Gtk.INVALID_LIST_POSITION

    @GObject.Property(type=Adw.ViewStack)
    def stack(self):
        split_view = getattr(self, "_split_view", None)

        if split_view is None:
            return None

        return split_view.get_content()

    @stack.setter
    def stack(self, widget):
        self._split_view.set_content(widget)
        self._show_selected_page()

    @GObject.Property(type=bool, default=False)
    def show_menu(self):
        split_view = getattr(self, "_split_view", None)

        if split_view is None:
            return False

        return split_view.props.show_sidebar

    @show_menu.setter
    def show_menu(self, shown):
        self._split_view.props.show_sidebar = shown

    @Gtk.Template.Callback()
    def _on_items_activated(self, _sidebar: Adw.Sidebar, _index: int) -> None:
        self._show_selected_page()
        self.props.show_menu = False

    @Gtk.Template.Callback()
    def _on_power_activated(self, sidebar: Adw.Sidebar, _index: int) -> None:
        sidebar.props.selected = Gtk.INVALID_LIST_POSITION
        self.props.show_menu = False
        self.activate_action("win.power", None)

    def _show_selected_page(self) -> None:
        item = self._items.get_selected_item()

        if self.props.stack is None or item is None:
            return

        self.props.stack.props.visible_child_name = item.props.tag
