# style_row.py
#
# Copyright 2026 Muqtadir
#
# SPDX-License-Identifier: GPL-3.0-or-later

import gi

gi.require_version("Gtk", "4.0")
gi.require_version("Adw", "1")

from gi.repository import Adw, GObject, Gtk

from slipspace.components.appearance.appearance import Appearance


@Gtk.Template(
    resource_path="/com/muqtxdir/slipspace/components/appearance/style-row.ui"
)
class StyleRow(Adw.ActionRow):
    __gtype_name__ = "StyleRow"

    prefer_dark = GObject.Property(type=bool, default=False)

    def __init__(self, appearance: Appearance = None, **kwargs):
        super().__init__(**kwargs)

        self._appearance = appearance if appearance is not None else Appearance()

        self.props.prefer_dark = self._appearance.props.prefer_dark

        self._appearance.bind_property(
            "available", self, "visible", GObject.BindingFlags.SYNC_CREATE
        )
        self._appearance.bind_property(
            "prefer-dark",
            self,
            "prefer-dark",
            GObject.BindingFlags.SYNC_CREATE | GObject.BindingFlags.BIDIRECTIONAL,
        )
