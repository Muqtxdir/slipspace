# ethernet_row.py
#
# Copyright 2026 Muqtadir
#
# SPDX-License-Identifier: GPL-3.0-or-later

import gi

gi.require_version("Gtk", "4.0")
gi.require_version("Adw", "1")

from gi.repository import Adw, GObject, Gtk

from slipspace.components.network.network import Network


@Gtk.Template(
    resource_path="/com/muqtxdir/slipspace/components/network/ethernet-row.ui"
)
class EthernetRow(Adw.ActionRow):
    __gtype_name__ = "EthernetRow"

    icon_name = GObject.Property(type=str, default="")

    def __init__(self, network: Network = None, **kwargs):
        super().__init__(**kwargs)

        self._network = network if network is not None else Network()
        self._network.bind_property(
            "wired-icon-name", self, "icon-name", GObject.BindingFlags.SYNC_CREATE
        )
        self._network.bind_property(
            "wired-subtitle", self, "subtitle", GObject.BindingFlags.SYNC_CREATE
        )
        self._network.bind_property(
            "wired-connected", self, "visible", GObject.BindingFlags.SYNC_CREATE
        )
