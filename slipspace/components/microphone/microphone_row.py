# microphone_row.py
#
# Copyright 2026 Muqtadir
#
# SPDX-License-Identifier: GPL-3.0-or-later

import gi

gi.require_version("Gtk", "4.0")
gi.require_version("Adw", "1")

from gi.repository import Adw, GObject, Gtk

from slipspace.components.microphone.microphone import Microphone

VOLUME_EPSILON = 0.001


@Gtk.Template(
    resource_path="/com/muqtxdir/slipspace/components/microphone/microphone-row.ui"
)
class MicrophoneRow(Adw.ExpanderRow):
    __gtype_name__ = "MicrophoneRow"

    icon_name = GObject.Property(type=str, default="")
    volume = GObject.Property(type=float, default=0.0)

    def __init__(self, microphone: Microphone = None, **kwargs):
        super().__init__(**kwargs)

        self._microphone = microphone if microphone is not None else Microphone()

        self.props.volume = self._microphone.props.volume
        self.props.enable_expansion = not self._microphone.props.mute

        self._microphone.bind_property(
            "icon-name", self, "icon-name", GObject.BindingFlags.SYNC_CREATE
        )
        self._microphone.bind_property(
            "subtitle", self, "subtitle", GObject.BindingFlags.SYNC_CREATE
        )
        self._microphone.bind_property(
            "has-microphone", self, "visible", GObject.BindingFlags.SYNC_CREATE
        )
        self._microphone.bind_property(
            "volume", self, "volume", GObject.BindingFlags.SYNC_CREATE
        )
        self._microphone.bind_property(
            "mute",
            self,
            "enable-expansion",
            GObject.BindingFlags.SYNC_CREATE,
            lambda _binding, muted: not muted,
        )

        self.connect("notify::volume", self._on_volume_changed)
        self.connect("notify::enable-expansion", self._on_expansion_changed)

    def _on_volume_changed(self, _object, _pspec):
        if abs(self._microphone.props.volume - self.props.volume) > VOLUME_EPSILON:
            self._microphone.props.volume = self.props.volume

    def _on_expansion_changed(self, _object, _pspec):
        muted = not self.props.enable_expansion

        if self._microphone.props.mute != muted:
            self._microphone.props.mute = muted
