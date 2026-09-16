# bluetooth_icon.py
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
    resource_path="/com/muqtxdir/slipspace/components/bluetooth/bluetooth-icon.ui"
)
class BluetoothIcon(Adw.Bin):
    __gtype_name__ = "BluetoothIcon"

    icon_name = GObject.Property(type=str, default="")

    def __init__(self, bluetooth: Bluetooth = None, **kwargs):
        super().__init__(**kwargs)

        self._bluetooth = bluetooth if bluetooth is not None else Bluetooth()
        self._bluetooth.bind_property(
            "icon-name", self, "icon-name", GObject.BindingFlags.SYNC_CREATE
        )
        self._bluetooth.bind_property(
            "available", self, "visible", GObject.BindingFlags.SYNC_CREATE
        )
