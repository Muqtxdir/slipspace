# powerprofiles_icon.py
#
# Copyright 2026 Muqtadir
#
# SPDX-License-Identifier: GPL-3.0-or-later

import gi

gi.require_version("Gtk", "4.0")
gi.require_version("Adw", "1")

from gi.repository import Adw, GObject, Gtk

from slipspace.components.powerprofiles.powerprofiles import PowerProfiles


@Gtk.Template(
    resource_path="/com/muqtxdir/slipspace/components/powerprofiles/powerprofiles-icon.ui"
)
class PowerProfilesIcon(Adw.Bin):
    __gtype_name__ = "PowerProfilesIcon"

    icon_name = GObject.Property(type=str, default="")

    def __init__(self, power_profiles: PowerProfiles = None, **kwargs):
        super().__init__(**kwargs)

        self._power = power_profiles if power_profiles is not None else PowerProfiles()
        self._power.bind_property(
            "icon-name", self, "icon-name", GObject.BindingFlags.SYNC_CREATE
        )
        self._power.bind_property(
            "available", self, "visible", GObject.BindingFlags.SYNC_CREATE
        )
