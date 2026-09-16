# datetime_label.py
#
# Copyright 2026 Muqtadir
#
# SPDX-License-Identifier: GPL-3.0-or-later

import gi

gi.require_version('Gtk', '4.0')
gi.require_version('Adw', '1')

from gi.repository import Adw, GObject, Gtk

from slipspace.components.datetime.clock import Clock


@Gtk.Template(resource_path='/com/muqtxdir/slipspace/components/datetime/datetime-label.ui')
class DatetimeLabel(Adw.Bin):

    __gtype_name__ = 'DatetimeLabel'

    time = GObject.Property(type=str, default='')

    def __init__(self, clock: Clock = None, **kwargs):
        super().__init__(**kwargs)

        self._clock = clock if clock is not None else Clock()
        self._clock.bind_property('time', self, 'time', GObject.BindingFlags.SYNC_CREATE)
