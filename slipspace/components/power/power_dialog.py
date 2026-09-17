# power_dialog.py
#
# Copyright 2026 Muqtadir
#
# SPDX-License-Identifier: GPL-3.0-or-later

import gi

gi.require_version("Adw", "1")

from gettext import gettext as _

from gi.repository import Adw, Gio


class PowerDialog(Adw.AlertDialog):
    __gtype_name__ = "PowerDialog"

    def __init__(self, **kwargs):
        super().__init__(
            heading=_("Goodbye"),
            body=_("What do you want to do?"),
            default_response="cancel",
            close_response="cancel",
            **kwargs,
        )

        self.add_response("cancel", _("_Cancel"))
        self.add_response("restart", _("_Restart"))
        self.add_response("power-off", _("_Power Off"))
        self.set_response_appearance("power-off", Adw.ResponseAppearance.DESTRUCTIVE)

        self.connect("response", self._on_response)

    def _on_response(self, _dialog, response: str) -> None:
        if response == "power-off":
            self._run("poweroff")
        elif response == "restart":
            self._run("reboot")

    def _run(self, command: str) -> None:
        Gio.Subprocess.new(["systemctl", command], Gio.SubprocessFlags.NONE)
