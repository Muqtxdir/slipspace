# clock.py
#
# Copyright 2026 Muqtadir
#
# SPDX-License-Identifier: GPL-3.0-or-later

import gi

gi.require_version('GnomeDesktop', '4.0')

from gi.repository import Gio, GLib, GnomeDesktop, GObject

from gettext import gettext as _

from slipspace.components.datetime.enums import ClockFormat

DATETIME_SCHEMA_ID = 'com.muqtxdir.slipspace.datetime'


class Clock(GObject.Object):

    __gtype_name__ = 'Clock'

    time_format = GObject.Property(type=str,
                                   default=ClockFormat.TWENTY_FOUR_HOUR)
    time = GObject.Property(type=str, default='')

    def __init__(self, settings: Gio.Settings = None, **kwargs):
        super().__init__(**kwargs)

        self._wall_clock = GnomeDesktop.WallClock()
        self._wall_clock.connect('notify::clock', self._on_changed)
        self.connect('notify::time-format', self._on_changed)

        if settings is None:
            settings = Gio.Settings.new(DATETIME_SCHEMA_ID)

        settings.bind('time-format', self, 'time-format',
                      Gio.SettingsBindFlags.GET)

        self._update()

    def _on_changed(self, _object, _pspec):
        self._update()

    def _now(self) -> GLib.DateTime:
        timezone = self._wall_clock.props.timezone

        if timezone is not None:
            return GLib.DateTime.new_now(timezone)

        return GLib.DateTime.new_now_local()

    def _format(self) -> str:
        if self.props.time_format == ClockFormat.TWELVE_HOUR:
            return _('%l:%M %p')

        return _('%H:%M')

    def _update(self) -> None:
        self.props.time = ' '.join(self._now().format(self._format()).split())
