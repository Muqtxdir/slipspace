# accents_row.py
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

SWATCH_CSS_CLASSES = ["selection-mode", "accent-swatch"]


@Gtk.Template(
    resource_path="/com/muqtxdir/slipspace/components/appearance/accents-row.ui"
)
class AccentsRow(Adw.ExpanderRow):
    __gtype_name__ = "AccentsRow"

    accent = GObject.Property(type=int, default=int(GDesktopEnums.AccentColor.BLUE))

    _swatches: Gtk.Box = Gtk.Template.Child("swatches")

    def __init__(self, appearance: Appearance = None, **kwargs):
        super().__init__(**kwargs)

        self._appearance = appearance if appearance is not None else Appearance()
        self._buttons: dict[GDesktopEnums.AccentColor, Gtk.CheckButton] = {}

        self._build_swatches()

        self._appearance.bind_property(
            "has-accent", self, "visible", GObject.BindingFlags.SYNC_CREATE
        )
        self._appearance.bind_property(
            "accent", self, "accent", GObject.BindingFlags.SYNC_CREATE
        )

        self.connect("notify::accent", self._on_accent_changed)
        self._select_swatch()

    def _build_swatches(self) -> None:
        group = None

        for accent in GDesktopEnums.AccentColor:
            button = Gtk.CheckButton(tooltip_text=accent_label(accent))
            for css_class in SWATCH_CSS_CLASSES + [accent_class(accent)]:
                button.add_css_class(css_class)

            if group is None:
                group = button
            else:
                button.set_group(group)

            button.connect("toggled", self._on_swatch_toggled, accent)

            self._buttons[accent] = button
            self._swatches.append(button)

    def _select_swatch(self) -> None:
        self._buttons[GDesktopEnums.AccentColor(self.props.accent)].set_active(True)

    def _on_accent_changed(self, _object, _pspec):
        self._select_swatch()

    def _on_swatch_toggled(self, button: Gtk.CheckButton, accent) -> None:
        if button.get_active() and self._appearance.props.accent != accent:
            self._appearance.props.accent = accent

    @Gtk.Template.Callback()
    def _get_accent_name(self, _object, accent: int) -> str:
        return accent_label(GDesktopEnums.AccentColor(accent))
