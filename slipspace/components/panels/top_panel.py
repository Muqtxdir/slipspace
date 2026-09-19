# top_panel.py
#
# Copyright 2026 Muqtadir
#
# SPDX-License-Identifier: GPL-3.0-or-later

import gi

gi.require_version("Gtk", "4.0")

from gi.repository import GObject, Gtk

from slipspace.components.quicksettings import QuickSettingsButton

GObject.type_ensure(QuickSettingsButton)


@Gtk.Template(resource_path="/com/muqtxdir/slipspace/components/panels/top-panel.ui")
class TopPanel(Gtk.CenterBox):
    __gtype_name__ = "TopPanel"
