# menu_item.py
#
# Copyright 2026 Muqtadir
#
# SPDX-License-Identifier: GPL-3.0-or-later

import gi

gi.require_version("Adw", "1")

from gi.repository import Adw, GObject


class MenuItem(Adw.SidebarItem):
    __gtype_name__ = "MenuItem"

    tag = GObject.Property(type=str, default="")
