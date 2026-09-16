# enums.py
#
# Copyright 2026 Muqtadir
#
# SPDX-License-Identifier: GPL-3.0-or-later

from enum import StrEnum


class ClockFormat(StrEnum):
    TWENTY_FOUR_HOUR = "24h"
    TWELVE_HOUR = "12h"
