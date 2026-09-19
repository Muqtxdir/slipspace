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

    show_icon = GObject.Property(type=bool, default=True)

    def __init__(self, network: Network = None, **kwargs):
        super().__init__(**kwargs)

        self._network = network if network is not None else Network()
        self._network.bind_property(
            "wired-subtitle", self, "subtitle", GObject.BindingFlags.SYNC_CREATE
        )
        self._network.bind_property(
            "wired-connected", self, "visible", GObject.BindingFlags.SYNC_CREATE
        )

        self._network.connect("notify::wired-icon-name", self._update_icon)
        self.connect("notify::show-icon", self._update_icon)
        self._update_icon()

    def _update_icon(self, *_args) -> None:
        self.props.icon_name = (
            self._network.props.wired_icon_name if self.props.show_icon else ""
        )
