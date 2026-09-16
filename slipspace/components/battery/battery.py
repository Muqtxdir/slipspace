# battery.py
#
# Copyright 2026 Muqtadir
#
# SPDX-License-Identifier: GPL-3.0-or-later

import gi

gi.require_version('AstalBattery', '0.1')

from gi.repository import AstalBattery, GObject


class Battery(GObject.Object):

    __gtype_name__ = 'Battery'

    icon_name = GObject.Property(type=str, default='')
    available = GObject.Property(type=bool, default=False)

    def __init__(self, device: AstalBattery.Device = None, **kwargs):
        super().__init__(**kwargs)

        self._device = (device if device is not None
                        else AstalBattery.get_default())

        if self._device is None:
            return

        for signal in ('notify::battery-icon-name', 'notify::is-battery',
                       'notify::is-present'):
            self._device.connect(signal, self._on_changed)

        self._update()

    def _on_changed(self, _object, _pspec):
        self._update()

    def _update(self) -> None:
        self.props.icon_name = self._device.props.battery_icon_name
        self.props.available = (self._device.props.is_battery
                                and self._device.props.is_present)
