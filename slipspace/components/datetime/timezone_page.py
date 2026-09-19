# timezone_page.py
#
# Copyright 2026 Muqtadir
#
# SPDX-License-Identifier: GPL-3.0-or-later

import gi

gi.require_version("Gtk", "4.0")
gi.require_version("Adw", "1")

from gi.repository import Adw, GObject, Gtk

from slipspace.components.datetime.clock import Clock
from slipspace.components.datetime.timezone import Timezone, TimezoneItem
from slipspace.components.datetime.timezone_item_row import TimezoneItemRow


@Gtk.Template(
    resource_path="/com/muqtxdir/slipspace/components/datetime/timezone-page.ui"
)
class TimezonePage(Adw.Bin):
    __gtype_name__ = "TimezonePage"

    selected = GObject.Property(type=str, default="")

    search_entry = Gtk.Template.Child()
    timezones = Gtk.Template.Child()

    def __init__(self, timezone: Timezone = None, **kwargs):
        super().__init__(**kwargs)

        self._timezone = timezone if timezone is not None else Timezone()
        self._timezone.load()
        self._top = self._timezone.props.timezone

        self._filter = Gtk.CustomFilter.new(self._match)

        self.timezones.bind_model(
            Gtk.FilterListModel(
                model=Gtk.SortListModel(
                    model=self._timezone.items,
                    sorter=Gtk.CustomSorter.new(self._compare),
                ),
                filter=self._filter,
            ),
            TimezoneItemRow,
        )

        self.connect("notify::selected", self._on_selected_changed)
        self.props.selected = self._top

        self._clock = Clock()
        self._clock.connect("notify::time", self._on_clock_time)
        self._on_clock_time(self._clock, None)

    def _compare(self, first: TimezoneItem, second: TimezoneItem, _data=None) -> int:
        keys = (
            (first.zone != self._top, first.name),
            (second.zone != self._top, second.name),
        )

        return (keys[0] > keys[1]) - (keys[0] < keys[1])

    def _match(self, item: TimezoneItem) -> bool:
        return item.matches(self.search_entry.props.text.casefold().split())

    def _on_selected_changed(self, _object, _pspec) -> None:
        for item in self._timezone.items:
            item.props.selected = item.zone == self.props.selected

    def _on_clock_time(self, clock: Clock, _pspec) -> None:
        for item in self._timezone.items:
            item.refresh(clock.props.time_format)

    @Gtk.Template.Callback()
    def _on_search_changed(self, _entry: Gtk.SearchEntry) -> None:
        self._filter.changed(Gtk.FilterChange.DIFFERENT)

    @Gtk.Template.Callback()
    def _on_row_activated(self, _list_box: Gtk.ListBox, row: TimezoneItemRow) -> None:
        self.props.selected = row.zone
