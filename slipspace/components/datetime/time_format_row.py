# time_format_row.py
#
# Copyright 2026 Muqtadir
#
# SPDX-License-Identifier: GPL-3.0-or-later

import gi

gi.require_version("Gtk", "4.0")
gi.require_version("Adw", "1")

from gi.repository import Adw, Gio, GObject, Gtk

from slipspace.components.datetime.clock import DATETIME_SCHEMA_ID
from slipspace.components.datetime.enums import ClockFormat


@Gtk.Template(
    resource_path="/com/muqtxdir/slipspace/components/datetime/time-format-row.ui"
)
class TimeFormatRow(Adw.ActionRow):
    __gtype_name__ = "TimeFormatRow"

    time_format = GObject.Property(type=str, default=ClockFormat.TWENTY_FOUR_HOUR)

    def __init__(self, settings: Gio.Settings = None, **kwargs):
        super().__init__(**kwargs)

        self._settings = (
            settings if settings is not None else Gio.Settings.new(DATETIME_SCHEMA_ID)
        )
        self._settings.bind(
            "time-format", self, "time-format", Gio.SettingsBindFlags.DEFAULT
        )
