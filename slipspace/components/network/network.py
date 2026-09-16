# network.py
#
# Copyright 2026 Muqtadir
#
# SPDX-License-Identifier: GPL-3.0-or-later

import gi

gi.require_version("AstalNetwork", "0.1")

from gettext import gettext as _

from gi.repository import AstalNetwork, GObject

WIRED_ICON = "network-wired-symbolic"
WIFI_ICON = "network-wireless-signal-good-symbolic"
OFFLINE_ICON = "network-offline-symbolic"


class Network(GObject.Object):
    __gtype_name__ = "Network"

    icon_name = GObject.Property(type=str, default=OFFLINE_ICON)
    available = GObject.Property(type=bool, default=False)

    has_wifi = GObject.Property(type=bool, default=False)
    wifi_icon_name = GObject.Property(type=str, default=WIFI_ICON)
    wifi_enabled = GObject.Property(type=bool, default=False)
    wifi_subtitle = GObject.Property(type=str, default="")

    wired_connected = GObject.Property(type=bool, default=False)
    wired_icon_name = GObject.Property(type=str, default=WIRED_ICON)
    wired_subtitle = GObject.Property(type=str, default="")

    def __init__(self, network: AstalNetwork.Network = None, **kwargs):
        super().__init__(**kwargs)

        self._wifi = None
        self._wired = None
        self._enabled_binding = None
        self._network = network if network is not None else AstalNetwork.get_default()

        if self._network is None:
            return

        for signal in ("notify::primary", "notify::wifi", "notify::wired"):
            self._network.connect(signal, self._on_changed)

        self._watch_wifi()
        self._watch_wired()
        self._update()

    def _on_changed(self, _object, _pspec):
        self._watch_wifi()
        self._watch_wired()
        self._update()

    def _watch_wifi(self) -> None:
        wifi = self._network.props.wifi

        if wifi is self._wifi:
            return

        if self._enabled_binding is not None:
            self._enabled_binding.unbind()
            self._enabled_binding = None

        self._wifi = wifi

        if wifi is None:
            return

        for signal in ("notify::icon-name", "notify::enabled", "notify::ssid"):
            wifi.connect(signal, self._on_changed)

        self._enabled_binding = wifi.bind_property(
            "enabled",
            self,
            "wifi-enabled",
            GObject.BindingFlags.SYNC_CREATE | GObject.BindingFlags.BIDIRECTIONAL,
        )

    def _watch_wired(self) -> None:
        wired = self._network.props.wired

        if wired is self._wired:
            return

        self._wired = wired

        if wired is None:
            return

        for signal in ("notify::icon-name", "notify::internet", "notify::state"):
            wired.connect(signal, self._on_changed)

    def _has_device(self) -> bool:
        return (
            self._network.props.wifi is not None
            or self._network.props.wired is not None
        )

    def _wifi_is_enabled(self) -> bool:
        wifi = self._network.props.wifi

        return wifi is not None and wifi.props.enabled

    def _icon(self) -> str:
        primary = self._network.props.primary

        if primary == AstalNetwork.Primary.WIRED:
            wired = self._network.props.wired

            return (
                wired.props.icon_name
                if wired is not None and wired.props.icon_name
                else WIRED_ICON
            )

        if primary == AstalNetwork.Primary.WIFI:
            wifi = self._network.props.wifi

            return (
                wifi.props.icon_name
                if wifi is not None and wifi.props.icon_name
                else WIFI_ICON
            )

        return OFFLINE_ICON

    def _update_wifi(self) -> None:
        wifi = self._network.props.wifi

        self.props.has_wifi = wifi is not None

        if wifi is None:
            return

        self.props.wifi_icon_name = wifi.props.icon_name or WIFI_ICON

        if not wifi.props.enabled:
            self.props.wifi_subtitle = _("Off")
        elif wifi.props.ssid:
            self.props.wifi_subtitle = wifi.props.ssid
        else:
            self.props.wifi_subtitle = _("Not connected")

    def _update_wired(self) -> None:
        wired = self._network.props.wired
        connected = (
            wired is not None
            and wired.props.internet == AstalNetwork.Internet.CONNECTED
        )

        self.props.wired_connected = connected

        if wired is None:
            return

        self.props.wired_icon_name = wired.props.icon_name or WIRED_ICON
        self.props.wired_subtitle = _("Connected") if connected else _("Not connected")

    def _update(self) -> None:
        self._update_wifi()
        self._update_wired()

        if not self._has_device():
            self.props.icon_name = OFFLINE_ICON
            self.props.available = False
            return

        self.props.icon_name = self._icon()
        self.props.available = (
            self._network.props.primary != AstalNetwork.Primary.UNKNOWN
            or self._wifi_is_enabled()
        )
