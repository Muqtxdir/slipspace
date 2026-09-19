# timezone_row.py
#
# Copyright 2026 Muqtadir
#
# SPDX-License-Identifier: GPL-3.0-or-later

import gi

gi.require_version("Gtk", "4.0")
gi.require_version("Adw", "1")

from gi.repository import Adw, GObject, Gtk

from slipspace.components.datetime.timezone import Timezone
from slipspace.components.datetime.timezone_page import TimezonePage


@Gtk.Template(
    resource_path="/com/muqtxdir/slipspace/components/datetime/timezone-row.ui"
)
class TimezoneRow(Adw.ActionRow):
    __gtype_name__ = "TimezoneRow"

    timezone = GObject.Property(type=str, default="")

    def __init__(self, timezone: Timezone = None, **kwargs):
        super().__init__(**kwargs)

        self._timezone = timezone if timezone is not None else Timezone()
        self._timezone.bind_property(
            "timezone", self, "timezone", GObject.BindingFlags.SYNC_CREATE
        )

    @Gtk.Template.Callback()
    def _on_activated(self, _row: Adw.ActionRow) -> None:
        page = TimezonePage(self._timezone)
        binding = self._timezone.bind_property(
            "timezone",
            page,
            "selected",
            GObject.BindingFlags.SYNC_CREATE | GObject.BindingFlags.BIDIRECTIONAL,
        )

        dialog = Adw.Dialog(
            child=page,
            content_width=600,
            content_height=600,
        )
        dialog.connect("closed", lambda *_args: binding.unbind())
        page.connect("notify::selected", lambda *_args: dialog.close())
        dialog.present(self)
