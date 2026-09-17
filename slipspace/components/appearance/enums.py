# enums.py
#
# Copyright 2026 Muqtadir
#
# SPDX-License-Identifier: GPL-3.0-or-later

import gi

gi.require_version("GDesktopEnums", "3.0")

from gettext import gettext as _

from gi.repository import GDesktopEnums


def accent_label(accent: GDesktopEnums.AccentColor) -> str:
    return {
        GDesktopEnums.AccentColor.BLUE: _("Blue"),
        GDesktopEnums.AccentColor.TEAL: _("Teal"),
        GDesktopEnums.AccentColor.GREEN: _("Green"),
        GDesktopEnums.AccentColor.YELLOW: _("Yellow"),
        GDesktopEnums.AccentColor.ORANGE: _("Orange"),
        GDesktopEnums.AccentColor.RED: _("Red"),
        GDesktopEnums.AccentColor.PINK: _("Pink"),
        GDesktopEnums.AccentColor.PURPLE: _("Purple"),
        GDesktopEnums.AccentColor.SLATE: _("Slate"),
    }[accent]


def accent_class(accent: GDesktopEnums.AccentColor) -> str:
    return accent.name.lower()
