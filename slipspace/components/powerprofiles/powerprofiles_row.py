# powerprofiles_row.py
#
# Copyright 2026 Muqtadir
#
# SPDX-License-Identifier: GPL-3.0-or-later

import gi

gi.require_version("Gtk", "4.0")
gi.require_version("Adw", "1")

from gi.repository import Adw, GObject, Gtk

from slipspace.components.powerprofiles.powerprofiles import (
    PowerProfiles,
    profile_label,
)


@Gtk.Template(
    resource_path="/com/muqtxdir/slipspace/components/powerprofiles/powerprofiles-row.ui"
)
class PowerProfilesRow(Adw.ComboRow):
    __gtype_name__ = "PowerProfilesRow"

    show_icon = GObject.Property(type=bool, default=True)

    def __init__(self, power_profiles: PowerProfiles = None, **kwargs):
        super().__init__(**kwargs)

        self._power = power_profiles if power_profiles is not None else PowerProfiles()
        self._profiles = self._power.profiles

        model = Gtk.StringList()

        for profile in self._profiles:
            model.append(profile_label(profile))

        self.set_model(model)

        self._power.connect("notify::icon-name", self._update_icon)
        self.connect("notify::show-icon", self._update_icon)
        self._update_icon()

        self._power.bind_property(
            "has-profiles", self, "visible", GObject.BindingFlags.SYNC_CREATE
        )

        if self._profiles:
            self._power.bind_property(
                "active-profile",
                self,
                "selected",
                GObject.BindingFlags.SYNC_CREATE | GObject.BindingFlags.BIDIRECTIONAL,
                self._profile_to_index,
                self._index_to_profile,
            )

    def _update_icon(self, *_args) -> None:
        self.props.icon_name = (
            self._power.props.icon_name if self.props.show_icon else ""
        )

    def _profile_to_index(self, _binding, profile):
        if profile in self._profiles:
            return self._profiles.index(profile)

        return 0

    def _index_to_profile(self, _binding, index):
        if 0 <= index < len(self._profiles):
            return self._profiles[index]

        return self._profiles[0]
