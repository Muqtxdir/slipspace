# speaker.py
#
# Copyright 2026 Muqtadir
#
# SPDX-License-Identifier: GPL-3.0-or-later

import gi

gi.require_version("AstalWp", "0.1")


from gi.repository import AstalWp, GObject


class Speaker(GObject.Object):
    __gtype_name__ = "Speaker"

    icon_name = GObject.Property(type=str, default="")
    available = GObject.Property(type=bool, default=False)
    volume = GObject.Property(type=float, default=0.0)
    mute = GObject.Property(type=bool, default=False)
    has_speaker = GObject.Property(type=bool, default=False)

    def __init__(self, wp: AstalWp.Wp = None, **kwargs):
        super().__init__(**kwargs)

        self._speaker = None
        self._volume_binding = None
        self._mute_binding = None
        self._wp = wp if wp is not None else AstalWp.get_default()

        if self._wp is None:
            return

        self._wp.connect("notify::default-speaker", self._on_changed)

        self._watch_speaker()
        self._update()

    def _on_changed(self, _object, _pspec):
        self._watch_speaker()
        self._update()

    def _watch_speaker(self) -> None:
        speaker = self._wp.props.default_speaker

        if speaker is self._speaker:
            return

        if self._volume_binding is not None:
            self._volume_binding.unbind()
            self._volume_binding = None

        if self._mute_binding is not None:
            self._mute_binding.unbind()
            self._mute_binding = None

        self._speaker = speaker

        if speaker is None:
            return

        speaker.connect("notify::volume-icon", self._on_changed)

        self._volume_binding = speaker.bind_property(
            "volume",
            self,
            "volume",
            GObject.BindingFlags.SYNC_CREATE | GObject.BindingFlags.BIDIRECTIONAL,
        )
        self._mute_binding = speaker.bind_property(
            "mute",
            self,
            "mute",
            GObject.BindingFlags.SYNC_CREATE | GObject.BindingFlags.BIDIRECTIONAL,
        )

    def _update(self) -> None:
        speaker = self._wp.props.default_speaker

        self.props.has_speaker = speaker is not None

        if speaker is None:
            self.props.available = False
            return

        self.props.icon_name = speaker.props.volume_icon
        self.props.available = True
