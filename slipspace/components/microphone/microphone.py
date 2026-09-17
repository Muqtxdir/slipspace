# microphone.py
#
# Copyright 2026 Muqtadir
#
# SPDX-License-Identifier: GPL-3.0-or-later

import gi

gi.require_version("AstalWp", "0.1")


from gi.repository import AstalWp, GObject


class Microphone(GObject.Object):
    __gtype_name__ = "Microphone"

    icon_name = GObject.Property(type=str, default="")
    available = GObject.Property(type=bool, default=False)
    volume = GObject.Property(type=float, default=0.0)
    mute = GObject.Property(type=bool, default=False)
    has_microphone = GObject.Property(type=bool, default=False)

    def __init__(self, wp: AstalWp.Wp = None, **kwargs):
        super().__init__(**kwargs)

        self._microphone = None
        self._volume_binding = None
        self._mute_binding = None
        self._wp = wp if wp is not None else AstalWp.get_default()

        if self._wp is None:
            return

        self._wp.connect("notify::default-microphone", self._on_changed)

        audio = self._wp.props.audio

        if audio is not None:
            audio.connect("recorder-added", self._on_recorders_changed)
            audio.connect("recorder-removed", self._on_recorders_changed)

        self._watch_microphone()
        self._update()

    def _on_changed(self, _object, _pspec):
        self._watch_microphone()
        self._update()

    def _on_recorders_changed(self, _audio, _stream):
        self._update()

    def _watch_microphone(self) -> None:
        microphone = self._wp.props.default_microphone

        if microphone is self._microphone:
            return

        if self._volume_binding is not None:
            self._volume_binding.unbind()
            self._volume_binding = None

        if self._mute_binding is not None:
            self._mute_binding.unbind()
            self._mute_binding = None

        self._microphone = microphone

        if microphone is None:
            return

        microphone.connect("notify::volume-icon", self._on_changed)
        microphone.connect("notify::mute", self._on_changed)

        self._volume_binding = microphone.bind_property(
            "volume",
            self,
            "volume",
            GObject.BindingFlags.SYNC_CREATE | GObject.BindingFlags.BIDIRECTIONAL,
        )
        self._mute_binding = microphone.bind_property(
            "mute",
            self,
            "mute",
            GObject.BindingFlags.SYNC_CREATE | GObject.BindingFlags.BIDIRECTIONAL,
        )

    def _in_use(self) -> bool:
        audio = self._wp.props.audio

        return audio is not None and bool(audio.props.recorders)

    def _update(self) -> None:
        microphone = self._wp.props.default_microphone

        self.props.has_microphone = microphone is not None

        if microphone is None:
            self.props.available = False
            return

        self.props.icon_name = microphone.props.volume_icon
        self.props.available = microphone.props.mute or self._in_use()
