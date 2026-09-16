# brightness.py
#
# Copyright 2026 Muqtadir
#
# SPDX-License-Identifier: GPL-3.0-or-later

import gi

gi.require_version("AstalBrightness", "0.1")

from gi.repository import AstalBrightness, GObject


class Brightness(GObject.Object):
    __gtype_name__ = "Brightness"

    brightness = GObject.Property(type=float, default=0.0)
    has_screen = GObject.Property(type=bool, default=False)

    def __init__(self, brightness: AstalBrightness.Brightness = None, **kwargs):
        super().__init__(**kwargs)

        self._screen = None
        self._brightness_binding = None
        self._brightness = (
            brightness
            if brightness is not None
            else AstalBrightness.Brightness.get_default()
        )

        if self._brightness is None:
            return

        self._brightness.connect("notify::screen", self._on_changed)

        self._watch_screen()
        self._update()

    def _on_changed(self, _object, _pspec):
        self._watch_screen()
        self._update()

    def _watch_screen(self) -> None:
        screen = self._brightness.props.screen

        if screen is self._screen:
            return

        if self._brightness_binding is not None:
            self._brightness_binding.unbind()
            self._brightness_binding = None

        self._screen = screen

        if screen is None:
            return

        self._brightness_binding = screen.bind_property(
            "brightness",
            self,
            "brightness",
            GObject.BindingFlags.SYNC_CREATE | GObject.BindingFlags.BIDIRECTIONAL,
        )

    def _update(self) -> None:
        self.props.has_screen = self._brightness.props.screen is not None
