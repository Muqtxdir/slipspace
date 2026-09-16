# window.py
#
# Copyright 2026 Muqtadir
#
# SPDX-License-Identifier: GPL-3.0-or-later

from gi.repository import Adw, GObject, Gtk

from slipspace.components.panel import Panel
from slipspace.components.quicksettings import QuickSettings

GObject.type_ensure(Panel)
GObject.type_ensure(QuickSettings)


@Gtk.Template(resource_path="/com/muqtxdir/slipspace/window.ui")
class SlipspaceWindow(Adw.ApplicationWindow):
    __gtype_name__ = "SlipspaceWindow"

    panel = Gtk.Template.Child()
    quick_settings = Gtk.Template.Child()

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.panel.bind_property(
            "show-settings",
            self.quick_settings,
            "show-settings",
            GObject.BindingFlags.SYNC_CREATE | GObject.BindingFlags.BIDIRECTIONAL,
        )
