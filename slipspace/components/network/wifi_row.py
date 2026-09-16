# wifi_row.py
#
# Copyright 2026 Muqtadir
#
# SPDX-License-Identifier: GPL-3.0-or-later

import gi

gi.require_version("Gtk", "4.0")
gi.require_version("Adw", "1")

from gi.repository import Adw, GObject, Gtk

from slipspace.components.network.network import Network


@Gtk.Template(resource_path="/com/muqtxdir/slipspace/components/network/wifi-row.ui")
class WifiRow(Adw.ActionRow):
    __gtype_name__ = "WifiRow"

    icon_name = GObject.Property(type=str, default="")
    wifi_enabled = GObject.Property(type=bool, default=False)

    def __init__(self, network: Network = None, **kwargs):
        super().__init__(**kwargs)

        self._network = network if network is not None else Network()
        self._network.bind_property(
            "wifi-icon-name", self, "icon-name", GObject.BindingFlags.SYNC_CREATE
        )
        self._network.bind_property(
            "wifi-subtitle", self, "subtitle", GObject.BindingFlags.SYNC_CREATE
        )
        self._network.bind_property(
            "has-wifi", self, "visible", GObject.BindingFlags.SYNC_CREATE
        )
        self._network.bind_property(
            "wifi-enabled",
            self,
            "wifi-enabled",
            GObject.BindingFlags.SYNC_CREATE | GObject.BindingFlags.BIDIRECTIONAL,
        )
