# timezone_item_row.py
#
# Copyright 2026 Muqtadir
#
# SPDX-License-Identifier: GPL-3.0-or-later

import gi

gi.require_version("Gtk", "4.0")
gi.require_version("Adw", "1")

from gi.repository import Adw, GObject, Gtk

from slipspace.components.datetime.timezone import TimezoneItem


@Gtk.Template(
    resource_path="/com/muqtxdir/slipspace/components/datetime/timezone-item-row.ui"
)
class TimezoneItemRow(Adw.ActionRow):
    __gtype_name__ = "TimezoneItemRow"

    selected = GObject.Property(type=bool, default=False)

    def __init__(self, item: TimezoneItem, **kwargs):
        super().__init__(**kwargs)

        self.zone = item.zone
        self.props.title = item.name

        item.bind_property(
            "subtitle", self, "subtitle", GObject.BindingFlags.SYNC_CREATE
        )
        item.bind_property(
            "selected", self, "selected", GObject.BindingFlags.SYNC_CREATE
        )
