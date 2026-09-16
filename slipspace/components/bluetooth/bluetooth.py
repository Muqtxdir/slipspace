# bluetooth.py
#
# Copyright 2026 Muqtadir
#
# SPDX-License-Identifier: GPL-3.0-or-later

import gi

gi.require_version("AstalBluetooth", "0.1")

from gettext import gettext as _
from gettext import ngettext

from gi.repository import AstalBluetooth, GObject

IDLE_ICON = "bluetooth-symbolic"
CONNECTED_ICON = "bluetooth-active-symbolic"


class Bluetooth(GObject.Object):
    __gtype_name__ = "Bluetooth"

    icon_name = GObject.Property(type=str, default=IDLE_ICON)
    available = GObject.Property(type=bool, default=False)

    has_adapter = GObject.Property(type=bool, default=False)
    powered = GObject.Property(type=bool, default=False)
    subtitle = GObject.Property(type=str, default="")

    def __init__(self, bluetooth: AstalBluetooth.Bluetooth = None, **kwargs):
        super().__init__(**kwargs)

        self._adapter = None
        self._powered_binding = None
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

        for signal in ("device-added", "device-removed"):
            self._bluetooth.connect(signal, self._on_devices_changed)

        self._watch_adapter()
        self._update()

    def _on_changed(self, _object, _pspec):
        self._watch_adapter()
        self._update()

    def _on_devices_changed(self, _bluetooth, _device):
        self._update()

    def _watch_adapter(self) -> None:
        adapter = self._bluetooth.props.adapter

        if adapter is self._adapter:
            return

        if self._powered_binding is not None:
            self._powered_binding.unbind()
            self._powered_binding = None

        self._adapter = adapter

        if adapter is None:
            return

        adapter.connect("notify::powered", self._on_changed)

        self._powered_binding = adapter.bind_property(
            "powered",
            self,
            "powered",
            GObject.BindingFlags.SYNC_CREATE | GObject.BindingFlags.BIDIRECTIONAL,
        )

    def _connected_devices(self) -> list:
        return [
            device
            for device in self._bluetooth.props.devices or []
            if device.props.connected
        ]

    def _subtitle(self) -> str:
        if not self._bluetooth.props.is_powered:
            return _("Off")

        devices = self._connected_devices()
        count = len(devices)

        if count == 0:
            return _("Not connected")

        if count == 1:
            name = devices[0].props.name or devices[0].props.address

            if name:
                return name

        return ngettext("%d device connected", "%d devices connected", count) % count

    def _update(self) -> None:
        connected = self._bluetooth.props.is_connected

        self.props.icon_name = CONNECTED_ICON if connected else IDLE_ICON
        self.props.has_adapter = self._bluetooth.props.adapter is not None
        self.props.subtitle = self._subtitle()
        self.props.available = (
            self.props.has_adapter and self._bluetooth.props.is_powered
        )
