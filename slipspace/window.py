# window.py
#
# Copyright 2026 Muqtadir
#
# SPDX-License-Identifier: GPL-3.0-or-later

from gi.repository import Adw
from gi.repository import GObject
from gi.repository import Gtk

from slipspace.components.panel import Panel

GObject.type_ensure(Panel)


@Gtk.Template(resource_path='/com/muqtxdir/slipspace/window.ui')
class SlipspaceWindow(Adw.ApplicationWindow):
    __gtype_name__ = 'SlipspaceWindow'

    label = Gtk.Template.Child()

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
