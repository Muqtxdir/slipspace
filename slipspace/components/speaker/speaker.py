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

    def __init__(self, wp: AstalWp.Wp = None, **kwargs):
        super().__init__(**kwargs)

        self._speaker = None
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

        self._speaker = speaker

        if speaker is None:
            return

        speaker.connect("notify::volume-icon", self._on_changed)

    def _update(self) -> None:
        speaker = self._wp.props.default_speaker

        if speaker is None:
            self.props.available = False
            return

        self.props.icon_name = speaker.props.volume_icon
        self.props.available = True
