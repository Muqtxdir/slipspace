# bluetooth_row.py
#
# Copyright 2026 Muqtadir
#
# SPDX-License-Identifier: GPL-3.0-or-later

import gi

gi.require_version("Gtk", "4.0")
gi.require_version("Adw", "1")

from gi.repository import Adw, GObject, Gtk

from slipspace.components.bluetooth.bluetooth import Bluetooth


@Gtk.Template(
    resource_path="/com/muqtxdir/slipspace/components/bluetooth/bluetooth-row.ui"
)
class BluetoothRow(Adw.ActionRow):
    __gtype_name__ = "BluetoothRow"

    icon_name = GObject.Property(type=str, default="")
    powered = GObject.Property(type=bool, default=False)

    def __init__(self, bluetooth: Bluetooth = None, **kwargs):
        super().__init__(**kwargs)

        self._bluetooth = bluetooth if bluetooth is not None else Bluetooth()
        self._bluetooth.bind_property(
            "icon-name", self, "icon-name", GObject.BindingFlags.SYNC_CREATE
        )
        self._bluetooth.bind_property(
            "subtitle", self, "subtitle", GObject.BindingFlags.SYNC_CREATE
        )
        self._bluetooth.bind_property(
            "has-adapter", self, "visible", GObject.BindingFlags.SYNC_CREATE
        )
        self._bluetooth.bind_property(
            "powered",
            self,
            "powered",
            GObject.BindingFlags.SYNC_CREATE | GObject.BindingFlags.BIDIRECTIONAL,
        )
