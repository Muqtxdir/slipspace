# speaker_icon.py
#
# Copyright 2026 Muqtadir
#
# SPDX-License-Identifier: GPL-3.0-or-later

import gi

gi.require_version("Gtk", "4.0")
gi.require_version("Adw", "1")

from gi.repository import Adw, GObject, Gtk

from slipspace.components.speaker.speaker import Speaker


@Gtk.Template(
    resource_path="/com/muqtxdir/slipspace/components/speaker/speaker-icon.ui"
)
class SpeakerIcon(Adw.Bin):
    __gtype_name__ = "SpeakerIcon"

    icon_name = GObject.Property(type=str, default="")

    def __init__(self, speaker: Speaker = None, **kwargs):
        super().__init__(**kwargs)

        self._speaker = speaker if speaker is not None else Speaker()
        self._speaker.bind_property(
            "icon-name", self, "icon-name", GObject.BindingFlags.SYNC_CREATE
        )
        self._speaker.bind_property(
            "available", self, "visible", GObject.BindingFlags.SYNC_CREATE
        )
