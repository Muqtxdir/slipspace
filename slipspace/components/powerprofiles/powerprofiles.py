# powerprofiles.py
#
# Copyright 2026 Muqtadir
#
# SPDX-License-Identifier: GPL-3.0-or-later

import gi

gi.require_version("AstalPowerProfiles", "0.1")

from gettext import gettext as _

from gi.repository import AstalPowerProfiles, Gio, GLib, GObject

DAEMON_NAMES = (
    "org.freedesktop.UPower.PowerProfiles",
    "net.hadess.PowerProfiles",
)

BALANCED_PROFILE = "balanced"

PROFILE_ICONS = {
    "power-saver": "power-profile-power-saver-symbolic",
    "balanced": "power-profile-balanced-symbolic",
    "performance": "power-profile-performance-symbolic",
}


def profile_icon(profile: str) -> str:
    return PROFILE_ICONS.get(profile, "")


def profile_label(profile: str) -> str:
    if profile == "power-saver":
        return _("Power Saver")

    if profile == "balanced":
        return _("Balanced")

    if profile == "performance":
        return _("Performance")

    return profile


class PowerProfiles(GObject.Object):
    __gtype_name__ = "PowerProfiles"

    active_profile = GObject.Property(type=str, default="")
    icon_name = GObject.Property(type=str, default="")
    available = GObject.Property(type=bool, default=False)
    has_profiles = GObject.Property(type=bool, default=False)

    def __init__(
        self, power_profiles: AstalPowerProfiles.PowerProfiles = None, **kwargs
    ):
        super().__init__(**kwargs)

        self._profiles = []
        self._power = (
            power_profiles
            if power_profiles is not None
            else AstalPowerProfiles.get_default()
        )

        if self._power is None:
            return

        self._profiles = self._read_profiles()

        self._power.bind_property(
            "active-profile",
            self,
            "active-profile",
            GObject.BindingFlags.SYNC_CREATE | GObject.BindingFlags.BIDIRECTIONAL,
        )
        self._power.bind_property(
            "icon-name", self, "icon-name", GObject.BindingFlags.SYNC_CREATE
        )

        self.connect("notify::active-profile", self._on_active_profile_changed)

        self.props.has_profiles = len(self._profiles) > 1
        self._update_available()

    def _on_active_profile_changed(self, _object, _pspec):
        self._update_available()

    def _update_available(self) -> None:
        self.props.available = (
            self.props.has_profiles and self.props.active_profile != BALANCED_PROFILE
        )

    @property
    def profiles(self) -> list:
        return list(self._profiles)

    def _read_profiles(self) -> list:
        for name in DAEMON_NAMES:
            try:
                proxy = Gio.DBusProxy.new_for_bus_sync(
                    Gio.BusType.SYSTEM,
                    Gio.DBusProxyFlags.NONE,
                    None,
                    name,
                    "/" + name.replace(".", "/"),
                    name,
                    None,
                )
            except GLib.Error:
                continue

            entries = proxy.get_cached_property("Profiles")

            if entries is None:
                continue

            return [
                entry["Profile"] for entry in entries.unpack() if "Profile" in entry
            ]

        return []
