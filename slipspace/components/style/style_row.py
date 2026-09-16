# style_row.py
#
# Copyright 2026 Muqtadir
#
# SPDX-License-Identifier: GPL-3.0-or-later

import gi

gi.require_version("Gtk", "4.0")
gi.require_version("Adw", "1")

from gi.repository import Adw, GObject, Gtk

from slipspace.components.style.style import Style


@Gtk.Template(resource_path="/com/muqtxdir/slipspace/components/style/style-row.ui")
class StyleRow(Adw.ActionRow):
    __gtype_name__ = "StyleRow"

    prefer_dark = GObject.Property(type=bool, default=False)

    def __init__(self, style: Style = None, **kwargs):
        super().__init__(**kwargs)

        self._style = style if style is not None else Style()

        self.props.prefer_dark = self._style.props.prefer_dark

        self._style.bind_property(
            "available", self, "visible", GObject.BindingFlags.SYNC_CREATE
        )
        self._style.bind_property(
            "prefer-dark",
            self,
            "prefer-dark",
            GObject.BindingFlags.SYNC_CREATE | GObject.BindingFlags.BIDIRECTIONAL,
        )
