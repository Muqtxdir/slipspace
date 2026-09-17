# microphone_row.py
#
# Copyright 2026 Muqtadir
#
# SPDX-License-Identifier: GPL-3.0-or-later

import gi

gi.require_version("Gtk", "4.0")
gi.require_version("Adw", "1")

from gettext import gettext as _

from gi.repository import Adw, GObject, Gtk

from slipspace.components.microphone.microphone import Microphone

VOLUME_EPSILON = 0.001


@Gtk.Template(
    resource_path="/com/muqtxdir/slipspace/components/microphone/microphone-row.ui"
)
class MicrophoneRow(Adw.PreferencesRow):
    __gtype_name__ = "MicrophoneRow"

    icon_name = GObject.Property(type=str, default="")
    volume = GObject.Property(type=float, default=0.0)
    mute = GObject.Property(type=bool, default=False)

    def __init__(self, microphone: Microphone = None, **kwargs):
        super().__init__(**kwargs)

        self._microphone = microphone if microphone is not None else Microphone()

        self.props.volume = self._microphone.props.volume

        self._microphone.bind_property(
            "icon-name", self, "icon-name", GObject.BindingFlags.SYNC_CREATE
        )
        self._microphone.bind_property(
            "has-microphone", self, "visible", GObject.BindingFlags.SYNC_CREATE
        )
        self._microphone.bind_property(
            "volume", self, "volume", GObject.BindingFlags.SYNC_CREATE
        )
        self._microphone.bind_property(
            "mute", self, "mute", GObject.BindingFlags.SYNC_CREATE
        )

        self.connect("notify::volume", self._on_volume_changed)

    def _on_volume_changed(self, _object, _pspec):
        if abs(self._microphone.props.volume - self.props.volume) > VOLUME_EPSILON:
            self._microphone.props.volume = self.props.volume

    @Gtk.Template.Callback()
    def _get_mute_tooltip(self, _object, mute: bool) -> str:
        return _("Unmute") if mute else _("Mute")

    @Gtk.Template.Callback()
    def _get_scale_sensitive(self, _object, mute: bool) -> bool:
        return not mute

    @Gtk.Template.Callback()
    def _on_mute_button_clicked(self, _button: Gtk.Button) -> None:
        self._microphone.props.mute = not self._microphone.props.mute
