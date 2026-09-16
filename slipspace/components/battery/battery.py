# battery.py
#
# Copyright 2026 Muqtadir
#
# SPDX-License-Identifier: GPL-3.0-or-later

import gi

gi.require_version('AstalBattery', '0.1')

from gi.repository import AstalBattery, Gio, GObject

from gettext import gettext as _

BATTERY_SCHEMA_ID = 'com.muqtxdir.slipspace.battery'


class Battery(GObject.Object):

    __gtype_name__ = 'Battery'

    icon_name = GObject.Property(type=str, default='')
    label = GObject.Property(type=str, default='')
    available = GObject.Property(type=bool, default=False)
    show_percentage = GObject.Property(type=bool, default=False)

    def __init__(self, device: AstalBattery.Device = None,
                 settings: Gio.Settings = None, **kwargs):
        super().__init__(**kwargs)

        self._device = (device if device is not None
                        else AstalBattery.get_default())

        if settings is None:
            settings = Gio.Settings.new(BATTERY_SCHEMA_ID)

        settings.bind('show-percentage', self, 'show-percentage',
                      Gio.SettingsBindFlags.GET)
        self.connect('notify::show-percentage', self._on_changed)

        if self._device is None:
            return

        for signal in ('notify::battery-icon-name', 'notify::is-battery',
                       'notify::is-present', 'notify::percentage'):
            self._device.connect(signal, self._on_changed)

        self._update()

    def _on_changed(self, _object, _pspec):
        if self._device is not None:
            self._update()

    def _percentage(self) -> str:
        if not self.props.show_percentage:
            return ''

        return _('%d%%') % round(self._device.props.percentage * 100)

    def _update(self) -> None:
        self.props.icon_name = self._device.props.battery_icon_name
        self.props.label = self._percentage()
        self.props.available = (self._device.props.is_battery
                                and self._device.props.is_present)
