# brightness_row.py
#
# Copyright 2026 Muqtadir
#
# SPDX-License-Identifier: GPL-3.0-or-later

import gi

gi.require_version("Gtk", "4.0")
gi.require_version("Adw", "1")

from gi.repository import Adw, GObject, Gtk

from slipspace.components.brightness.brightness import Brightness

BRIGHTNESS_EPSILON = 0.001


@Gtk.Template(
    resource_path="/com/muqtxdir/slipspace/components/brightness/brightness-row.ui"
)
class BrightnessRow(Adw.PreferencesRow):
    __gtype_name__ = "BrightnessRow"

    brightness = GObject.Property(type=float, default=0.0)

    def __init__(self, brightness: Brightness = None, **kwargs):
        super().__init__(**kwargs)

        self._brightness = brightness if brightness is not None else Brightness()

        self.props.brightness = self._brightness.props.brightness

        self._brightness.bind_property(
            "has-screen", self, "visible", GObject.BindingFlags.SYNC_CREATE
        )
        self._brightness.bind_property(
            "brightness", self, "brightness", GObject.BindingFlags.SYNC_CREATE
        )

        self.connect("notify::brightness", self._on_brightness_changed)

    def _on_brightness_changed(self, _object, _pspec):
        current = self._brightness.props.brightness

        if abs(current - self.props.brightness) > BRIGHTNESS_EPSILON:
            self._brightness.props.brightness = self.props.brightness
