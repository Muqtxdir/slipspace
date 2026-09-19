# timezone.py
#
# Copyright 2026 Muqtadir
#
# SPDX-License-Identifier: GPL-3.0-or-later

from datetime import datetime
from gettext import gettext as _
from zoneinfo import ZoneInfo, available_timezones

from gi.repository import Gio, GLib, GObject

from slipspace.components.datetime.clock import DATETIME_SCHEMA_ID
from slipspace.components.datetime.enums import ClockFormat

TIMEDATE1_NAME = "org.freedesktop.timedate1"
TIMEDATE1_PATH = "/org/freedesktop/timedate1"
PROPERTIES_INTERFACE = "org.freedesktop.DBus.Properties"
TIMEZONE_KEY = "timezone"


class TimezoneItem(GObject.Object):
    __gtype_name__ = "TimezoneItem"

    subtitle = GObject.Property(type=str, default="")
    selected = GObject.Property(type=bool, default=False)

    def __init__(self, zone: str, **kwargs):
        super().__init__(**kwargs)

        self.zone = zone
        self.name = zone.rsplit("/", 1)[-1].replace("_", " ")

        self._search_text = zone.replace("_", " ").casefold()
        self._timezone = ZoneInfo(zone)

    def matches(self, terms: list[str]) -> bool:
        return all(term in self._search_text for term in terms)

    def refresh(self, time_format: str) -> None:
        if time_format == ClockFormat.TWELVE_HOUR:
            # Translators: a row subtitle in the timezone dialog, as strftime
            # directives: the 12-hour time, then the weekday, day, month and year.
            subtitle_format = _("%l:%M %p • %A, %d %B %Y")
        else:
            # Translators: a row subtitle in the timezone dialog, as strftime
            # directives: the 24-hour time, then the weekday, day, month and year.
            subtitle_format = _("%H:%M • %A, %d %B %Y")

        subtitle = datetime.now(self._timezone).strftime(subtitle_format)

        self.props.subtitle = " ".join(subtitle.split())


class Timezone(GObject.Object):
    __gtype_name__ = "Timezone"

    timezone = GObject.Property(type=str, default="")

    def __init__(self, settings: Gio.Settings = None, **kwargs):
        super().__init__(**kwargs)

        self.items = Gio.ListStore(item_type=TimezoneItem)

        self._system = None
        self._settings = (
            settings if settings is not None else Gio.Settings.new(DATETIME_SCHEMA_ID)
        )
        self._settings.bind(
            TIMEZONE_KEY, self, "timezone", Gio.SettingsBindFlags.DEFAULT
        )

        self._bus = Gio.bus_get_sync(Gio.BusType.SYSTEM, None)
        self._bus.signal_subscribe(
            TIMEDATE1_NAME,
            PROPERTIES_INTERFACE,
            "PropertiesChanged",
            TIMEDATE1_PATH,
            None,
            Gio.DBusSignalFlags.NONE,
            self._on_properties_changed,
        )

        self.connect("notify::timezone", self._on_timezone_changed)

        self._read()

    def load(self) -> None:
        if self.items.get_n_items():
            return

        for zone in sorted(available_timezones()):
            self.items.append(TimezoneItem(zone))

    def _on_timezone_changed(self, _object, _pspec) -> None:
        if self._system is None or self.props.timezone == self._system:
            return

        self._bus.call(
            TIMEDATE1_NAME,
            TIMEDATE1_PATH,
            TIMEDATE1_NAME,
            "SetTimezone",
            GLib.Variant("(sb)", (self.props.timezone, True)),
            None,
            Gio.DBusCallFlags.NONE,
            -1,
            None,
            self._on_set_timezone,
        )

    def _read(self) -> None:
        self._bus.call(
            TIMEDATE1_NAME,
            TIMEDATE1_PATH,
            PROPERTIES_INTERFACE,
            "Get",
            GLib.Variant("(ss)", (TIMEDATE1_NAME, "Timezone")),
            GLib.VariantType("(v)"),
            Gio.DBusCallFlags.NONE,
            -1,
            None,
            self._on_read_timezone,
        )

    def _on_read_timezone(
        self, connection: Gio.DBusConnection, result: Gio.AsyncResult
    ):
        self._system = connection.call_finish(result).unpack()[0]
        self.props.timezone = self._system

    def _on_properties_changed(
        self, _connection, _sender, _path, _interface, _signal, parameters
    ) -> None:
        if "Timezone" in parameters.unpack()[1]:
            self._read()

    def _on_set_timezone(self, connection: Gio.DBusConnection, result: Gio.AsyncResult):
        connection.call_finish(result)
