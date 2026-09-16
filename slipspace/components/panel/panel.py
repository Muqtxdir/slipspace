# panel.py
#
# Copyright 2026 Muqtadir
#
# SPDX-License-Identifier: GPL-3.0-or-later

import gi

gi.require_version("Gtk", "4.0")
gi.require_version("Adw", "1")

from gi.repository import Adw, GObject, Gtk

from slipspace.components.battery import BatteryIcon
from slipspace.components.bluetooth import BluetoothIcon
from slipspace.components.datetime import DatetimeLabel
from slipspace.components.microphone import MicrophoneIcon
from slipspace.components.network import NetworkIcon
from slipspace.components.speaker import SpeakerIcon

GObject.type_ensure(BatteryIcon)
GObject.type_ensure(BluetoothIcon)
GObject.type_ensure(DatetimeLabel)
GObject.type_ensure(MicrophoneIcon)
GObject.type_ensure(NetworkIcon)
GObject.type_ensure(SpeakerIcon)


@Gtk.Template(resource_path="/com/muqtxdir/slipspace/components/panel/panel.ui")
class Panel(Adw.Bin):
    __gtype_name__ = "Panel"
