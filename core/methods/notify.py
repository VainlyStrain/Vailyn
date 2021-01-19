#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
_____, ___
   '+ .;
    , ;
     .

       .
     .;.
     .;
      :
      ,


┌─[Vailyn]─[~]
└──╼ VainlyStrain
"""


import os

import core.variables as variables

from core.config import DESKTOP_NOTIFY
from core.variables import SEPARATOR

if variables.adv_li and DESKTOP_NOTIFY:
    import notify2


def notify(message):
    """
    Display a notification. Used when further input is needed,
    or the scan is finished. You can configure & disable
    notifications in the config.py file.

    @params:
        message - message to show in the notification box
    """

    if DESKTOP_NOTIFY and variables.adv_li:
        icon = SEPARATOR.join([
            os.path.dirname(os.path.realpath("__main__")),
            "core",
            "qt5",
            "icons",
            "tid.png",
        ])

        notification = notify2.Notification(
            "Vailyn",
            message=message,
            icon=icon,
        )

        notification.show()
