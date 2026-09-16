# style.py
#
# Copyright 2026 Muqtadir
#
# SPDX-License-Identifier: GPL-3.0-or-later

from gi.repository import Gio, GObject

INTERFACE_SCHEMA_ID = "org.gnome.desktop.interface"
COLOR_SCHEME_KEY = "color-scheme"
PREFER_DARK = "prefer-dark"
DEFAULT_SCHEME = "default"


class Style(GObject.Object):
    __gtype_name__ = "Style"

    prefer_dark = GObject.Property(type=bool, default=False)
    available = GObject.Property(type=bool, default=False)

    def __init__(self, settings: Gio.Settings = None, **kwargs):
        super().__init__(**kwargs)

        self._settings = settings if settings is not None else self._lookup_settings()

        if self._settings is None:
            return

        self.props.available = True
        self.props.prefer_dark = self._current_scheme() == PREFER_DARK

        self._settings.connect("changed::" + COLOR_SCHEME_KEY, self._on_scheme_changed)
        self.connect("notify::prefer-dark", self._on_prefer_dark_changed)

    def _lookup_settings(self) -> Gio.Settings:
        source = Gio.SettingsSchemaSource.get_default()

        if source is None or source.lookup(INTERFACE_SCHEMA_ID, True) is None:
            return None

        return Gio.Settings.new(INTERFACE_SCHEMA_ID)

    def _current_scheme(self) -> str:
        return self._settings.get_string(COLOR_SCHEME_KEY)

    def _on_scheme_changed(self, _settings, _key):
        self.props.prefer_dark = self._current_scheme() == PREFER_DARK

    def _on_prefer_dark_changed(self, _object, _pspec):
        wanted = PREFER_DARK if self.props.prefer_dark else DEFAULT_SCHEME

        if self._current_scheme() != wanted:
            self._settings.set_string(COLOR_SCHEME_KEY, wanted)
