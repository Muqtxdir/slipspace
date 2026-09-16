# network.py
#
# Copyright 2026 Muqtadir
#
# SPDX-License-Identifier: GPL-3.0-or-later

import gi

gi.require_version('AstalNetwork', '0.1')

from gi.repository import AstalNetwork, GObject

WIRED_ICON = 'network-wired-symbolic'
WIFI_ICON = 'network-wireless-signal-good-symbolic'
OFFLINE_ICON = 'network-offline-symbolic'


class Network(GObject.Object):

    __gtype_name__ = 'Network'

    icon_name = GObject.Property(type=str, default=OFFLINE_ICON)
    available = GObject.Property(type=bool, default=False)

    def __init__(self, network: AstalNetwork.Network = None, **kwargs):
        super().__init__(**kwargs)

        self._wifi = None
        self._network = (network if network is not None
                         else AstalNetwork.get_default())

        if self._network is None:
            return

        for signal in ('notify::primary', 'notify::wifi', 'notify::wired'):
            self._network.connect(signal, self._on_changed)

        self._watch_wifi()
        self._update()

    def _on_changed(self, _object, _pspec):
        self._watch_wifi()
        self._update()

    def _watch_wifi(self) -> None:
        wifi = self._network.props.wifi

        if wifi is self._wifi:
            return

        self._wifi = wifi

        if wifi is None:
            return

        wifi.connect('notify::icon-name', self._on_changed)
        wifi.connect('notify::enabled', self._on_changed)

    def _has_device(self) -> bool:
        return (self._network.props.wifi is not None
                or self._network.props.wired is not None)

    def _wifi_enabled(self) -> bool:
        wifi = self._network.props.wifi

        return wifi is not None and wifi.props.enabled

    def _icon(self) -> str:
        primary = self._network.props.primary

        if primary == AstalNetwork.Primary.WIRED:
            wired = self._network.props.wired

            return (wired.props.icon_name if wired is not None
                    and wired.props.icon_name else WIRED_ICON)

        if primary == AstalNetwork.Primary.WIFI:
            wifi = self._network.props.wifi

            return (wifi.props.icon_name if wifi is not None
                    and wifi.props.icon_name else WIFI_ICON)

        return OFFLINE_ICON

    def _update(self) -> None:
        if not self._has_device():
            self.props.icon_name = OFFLINE_ICON
            self.props.available = False
            return

        self.props.icon_name = self._icon()
        self.props.available = (
            self._network.props.primary != AstalNetwork.Primary.UNKNOWN
            or self._wifi_enabled())
