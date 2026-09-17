# window.py
#
# Copyright 2026 Muqtadir
#
# SPDX-License-Identifier: GPL-3.0-or-later

from gi.repository import Adw, Gio, GObject, Gtk

from slipspace.components.menu import MenuOverlay
from slipspace.components.power import PowerDialog
from slipspace.components.quicksettings import (
    QuickSettingsButton,
    QuickSettingsOverlay,
)

GObject.type_ensure(QuickSettingsOverlay)
GObject.type_ensure(QuickSettingsButton)
GObject.type_ensure(MenuOverlay)


@Gtk.Template(resource_path="/com/muqtxdir/slipspace/window.ui")
class SlipspaceWindow(Adw.ApplicationWindow):
    __gtype_name__ = "SlipspaceWindow"

    quick_settings_overlay = Gtk.Template.Child()
    menu_overlay = Gtk.Template.Child()

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.add_action(
            Gio.PropertyAction.new(
                "quick-settings", self.quick_settings_overlay, "show-settings"
            )
        )
        self.add_action(Gio.PropertyAction.new("menu", self.menu_overlay, "show-menu"))

        power = Gio.SimpleAction.new("power", None)
        power.connect("activate", self._on_power_activate)
        self.add_action(power)

        self.quick_settings_overlay.connect(
            "notify::show-settings", self._on_quick_settings_shown
        )
        self.menu_overlay.connect("notify::show-menu", self._on_menu_shown)

    def _on_power_activate(self, _action, _parameter):
        PowerDialog().present(self)

    def _on_quick_settings_shown(self, _object, _pspec):
        if self.quick_settings_overlay.props.show_settings:
            self.menu_overlay.props.show_menu = False

    def _on_menu_shown(self, _object, _pspec):
        if self.menu_overlay.props.show_menu:
            self.quick_settings_overlay.props.show_settings = False
