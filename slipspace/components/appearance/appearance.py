# appearance.py
#
# Copyright 2026 Muqtadir
#
# SPDX-License-Identifier: GPL-3.0-or-later

import gi

gi.require_version("GDesktopEnums", "3.0")

from gi.repository import GDesktopEnums, Gio, GObject

INTERFACE_SCHEMA_ID = "org.gnome.desktop.interface"
COLOR_SCHEME_KEY = "color-scheme"
ACCENT_COLOR_KEY = "accent-color"


class Appearance(GObject.Object):
    __gtype_name__ = "Appearance"

    available = GObject.Property(type=bool, default=False)
    has_accent = GObject.Property(type=bool, default=False)
    color_scheme = GObject.Property(
        type=int, default=int(GDesktopEnums.ColorScheme.DEFAULT)
    )
    accent = GObject.Property(type=int, default=int(GDesktopEnums.AccentColor.BLUE))

    def __init__(self, settings: Gio.Settings = None, **kwargs):
        super().__init__(**kwargs)

        self._settings = settings if settings is not None else self._lookup_settings()

        if self._settings is None:
            return

        self.props.available = True
        self.props.color_scheme = self._settings.get_enum(COLOR_SCHEME_KEY)

        self._settings.connect("changed::" + COLOR_SCHEME_KEY, self._on_scheme_changed)
        self.connect("notify::color-scheme", self._on_color_scheme_property_changed)

        self.props.has_accent = self._settings.props.settings_schema.has_key(
            ACCENT_COLOR_KEY
        )

        if not self.props.has_accent:
            return

        self.props.accent = self._settings.get_enum(ACCENT_COLOR_KEY)

        self._settings.connect("changed::" + ACCENT_COLOR_KEY, self._on_accent_changed)
        self.connect("notify::accent", self._on_accent_property_changed)

    def _lookup_settings(self) -> Gio.Settings:
        source = Gio.SettingsSchemaSource.get_default()

        if source is None or source.lookup(INTERFACE_SCHEMA_ID, True) is None:
            return None

        return Gio.Settings.new(INTERFACE_SCHEMA_ID)

    def _on_scheme_changed(self, _settings, _key):
        self.props.color_scheme = self._settings.get_enum(COLOR_SCHEME_KEY)

    def _on_color_scheme_property_changed(self, _object, _pspec):
        if self._settings.get_enum(COLOR_SCHEME_KEY) != self.props.color_scheme:
            self._settings.set_enum(COLOR_SCHEME_KEY, self.props.color_scheme)

    def _on_accent_changed(self, _settings, _key):
        self.props.accent = self._settings.get_enum(ACCENT_COLOR_KEY)

    def _on_accent_property_changed(self, _object, _pspec):
        if self._settings.get_enum(ACCENT_COLOR_KEY) != self.props.accent:
            self._settings.set_enum(ACCENT_COLOR_KEY, self.props.accent)
