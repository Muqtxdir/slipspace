# appearance_row.py
#
# Copyright 2026 Muqtadir
#
# SPDX-License-Identifier: GPL-3.0-or-later

import gi

gi.require_version("Gtk", "4.0")
gi.require_version("Adw", "1")
gi.require_version("GDesktopEnums", "3.0")

from gi.repository import Adw, GDesktopEnums, GObject, Gtk

from slipspace.components.appearance.appearance import Appearance
from slipspace.components.appearance.enums import accent_class, accent_label


@Gtk.Template(
    resource_path="/com/muqtxdir/slipspace/components/appearance/appearance-row.ui"
)
class AppearanceRow(Adw.PreferencesRow):
    __gtype_name__ = "AppearanceRow"

    accent = GObject.Property(type=int, default=int(GDesktopEnums.AccentColor.BLUE))

    _default_tile: Gtk.ToggleButton = Gtk.Template.Child("default_tile")
    _dark_tile: Gtk.ToggleButton = Gtk.Template.Child("dark_tile")
    _swatches: Adw.WrapBox = Gtk.Template.Child("swatches")

    def __init__(self, appearance: Appearance = None, **kwargs):
        super().__init__(**kwargs)

        self._appearance = appearance if appearance is not None else Appearance()
        self._buttons: dict[GDesktopEnums.AccentColor, Gtk.CheckButton] = {}

        self._build_swatches()

        self._appearance.bind_property(
            "available", self, "visible", GObject.BindingFlags.SYNC_CREATE
        )
        self._appearance.bind_property(
            "has-accent", self._swatches, "visible", GObject.BindingFlags.SYNC_CREATE
        )
        self._appearance.bind_property(
            "accent", self, "accent", GObject.BindingFlags.SYNC_CREATE
        )

        self._appearance.connect("notify::color-scheme", self._on_color_scheme_changed)
        self._default_tile.connect("toggled", self._on_tile_toggled)
        self._dark_tile.connect("toggled", self._on_tile_toggled)

        self.connect("notify::accent", self._on_accent_changed)
        self._update_tiles()
        self._select_swatch()

    def _build_swatches(self) -> None:
        group = None

        for accent in GDesktopEnums.AccentColor:
            button = Gtk.CheckButton(tooltip_text=accent_label(accent))
            button.add_css_class("selection-mode")
            button.add_css_class("accent-swatch")
            button.add_css_class(accent_class(accent))

            if group is None:
                group = button
            else:
                button.set_group(group)

            button.connect("toggled", self._on_swatch_toggled, accent)

            self._buttons[accent] = button
            self._swatches.append(button)

    def _update_tiles(self) -> None:
        match self._appearance.props.color_scheme:
            case GDesktopEnums.ColorScheme.DEFAULT:
                self._default_tile.props.active = True
            case GDesktopEnums.ColorScheme.PREFER_DARK:
                self._dark_tile.props.active = True
            case _:
                self._default_tile.props.active = False
                self._dark_tile.props.active = False

    def _on_color_scheme_changed(self, _object, _pspec) -> None:
        self._update_tiles()

    def _on_tile_toggled(self, _button: Gtk.ToggleButton) -> None:
        if self._default_tile.props.active:
            self._appearance.props.color_scheme = int(GDesktopEnums.ColorScheme.DEFAULT)
        elif self._dark_tile.props.active:
            self._appearance.props.color_scheme = int(
                GDesktopEnums.ColorScheme.PREFER_DARK
            )

    def _select_swatch(self) -> None:
        self._buttons[GDesktopEnums.AccentColor(self.props.accent)].set_active(True)

    def _on_accent_changed(self, _object, _pspec):
        self._select_swatch()

    def _on_swatch_toggled(self, button: Gtk.CheckButton, accent) -> None:
        if button.get_active() and self._appearance.props.accent != accent:
            self._appearance.props.accent = accent
