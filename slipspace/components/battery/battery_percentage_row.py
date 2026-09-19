# battery_percentage_row.py
#
# Copyright 2026 Muqtadir
#
# SPDX-License-Identifier: GPL-3.0-or-later

import gi

gi.require_version("Gtk", "4.0")
gi.require_version("Adw", "1")

from gi.repository import Adw, GObject, Gtk

from slipspace.components.battery.battery import Battery


@Gtk.Template(
    resource_path="/com/muqtxdir/slipspace/components/battery/battery-percentage-row.ui"
)
class BatteryPercentageRow(Adw.ActionRow):
    __gtype_name__ = "BatteryPercentageRow"

    show_percentage = GObject.Property(type=bool, default=False)

    def __init__(self, battery: Battery = None, **kwargs):
        super().__init__(**kwargs)

        self._battery = battery if battery is not None else Battery()
        self._battery.bind_property(
            "available", self, "visible", GObject.BindingFlags.SYNC_CREATE
        )
        self._battery.bind_property(
            "show-percentage",
            self,
            "show-percentage",
            GObject.BindingFlags.SYNC_CREATE | GObject.BindingFlags.BIDIRECTIONAL,
        )
