# quicksettings.py
#
# Copyright 2026 Muqtadir
#
# SPDX-License-Identifier: GPL-3.0-or-later

import gi

gi.require_version("Gtk", "4.0")
gi.require_version("Adw", "1")

from gi.repository import Adw, GObject, Gtk

from slipspace.components.appearance import StyleRow
from slipspace.components.bluetooth import BluetoothRow
from slipspace.components.brightness import BrightnessRow
from slipspace.components.microphone import MicrophoneRow
from slipspace.components.network import LanRow, WifiRow
from slipspace.components.powerprofiles import PowerProfilesRow
from slipspace.components.quicksettings.quicksettings_button import (
    QuickSettingsButton,
)
from slipspace.components.speaker import SpeakerRow

GObject.type_ensure(BluetoothRow)
GObject.type_ensure(QuickSettingsButton)
GObject.type_ensure(BrightnessRow)
GObject.type_ensure(StyleRow)
GObject.type_ensure(MicrophoneRow)
GObject.type_ensure(LanRow)
GObject.type_ensure(PowerProfilesRow)
GObject.type_ensure(WifiRow)
GObject.type_ensure(SpeakerRow)


@Gtk.Template(
    resource_path="/com/muqtxdir/slipspace/components/quicksettings/quicksettings.ui"
)
class QuickSettings(Adw.Bin):
    __gtype_name__ = "QuickSettings"

    split_view = Gtk.Template.Child()

    show_settings = GObject.Property(type=bool, default=False)

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.bind_property(
            "show-settings",
            self.split_view,
            "show-sidebar",
            GObject.BindingFlags.SYNC_CREATE | GObject.BindingFlags.BIDIRECTIONAL,
        )

    @GObject.Property(type=Gtk.Widget)
    def content(self):
        split_view = getattr(self, "split_view", None)

        if split_view is None:
            return None

        return split_view.get_content()

    @content.setter
    def content(self, widget):
        self.split_view.set_content(widget)

    @Gtk.Template.Callback()
    def _on_dismiss_clicked(self, _button):
        self.props.show_settings = False
