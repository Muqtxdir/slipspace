# bluetooth.py
#
# Copyright 2026 Muqtadir
#
# SPDX-License-Identifier: GPL-3.0-or-later

import gi

gi.require_version("AstalBluetooth", "0.1")

from gi.repository import AstalBluetooth, GObject

IDLE_ICON = "bluetooth-symbolic"
CONNECTED_ICON = "bluetooth-active-symbolic"


class Bluetooth(GObject.Object):
    __gtype_name__ = "Bluetooth"

    icon_name = GObject.Property(type=str, default=IDLE_ICON)
    available = GObject.Property(type=bool, default=False)

    def __init__(self, bluetooth: AstalBluetooth.Bluetooth = None, **kwargs):
        super().__init__(**kwargs)

        self._bluetooth = (
            bluetooth if bluetooth is not None else AstalBluetooth.get_default()
        )

        if self._bluetooth is None:
            return

        for signal in (
            "notify::adapter",
            "notify::is-powered",
            "notify::is-connected",
        ):
            self._bluetooth.connect(signal, self._on_changed)

        self._update()

    def _on_changed(self, _object, _pspec):
        self._update()

    def _update(self) -> None:
        connected = self._bluetooth.props.is_connected

        self.props.icon_name = CONNECTED_ICON if connected else IDLE_ICON
        self.props.available = (
            self._bluetooth.props.adapter is not None
            and self._bluetooth.props.is_powered
        )
