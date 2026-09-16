# microphone_icon.py
#
# Copyright 2026 Muqtadir
#
# SPDX-License-Identifier: GPL-3.0-or-later

import gi

gi.require_version("Gtk", "4.0")
gi.require_version("Adw", "1")

from gi.repository import Adw, GObject, Gtk

from slipspace.components.microphone.microphone import Microphone


@Gtk.Template(
    resource_path="/com/muqtxdir/slipspace/components/microphone/microphone-icon.ui"
)
class MicrophoneIcon(Adw.Bin):
    __gtype_name__ = "MicrophoneIcon"

    icon_name = GObject.Property(type=str, default="")

    def __init__(self, microphone: Microphone = None, **kwargs):
        super().__init__(**kwargs)

        self._microphone = microphone if microphone is not None else Microphone()
        self._microphone.bind_property(
            "icon-name", self, "icon-name", GObject.BindingFlags.SYNC_CREATE
        )
        self._microphone.bind_property(
            "available", self, "visible", GObject.BindingFlags.SYNC_CREATE
        )
