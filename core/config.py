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


"""
Optional Vailyn Features
"""

# Display desktop notifications on certain events.
# Set False to disable. (default: True)
DESKTOP_NOTIFY = True

# Check if response matches /etc/passwd REGEX
# if that file is used. (default: True)
REGEX_CHECK = True


"""
Output Options
"""

# Only use ASCII characters in output
# (default: False)
ASCII_ONLY = False

# Do not flush the terminal when starting
# the tool (default: False)
NO_CLEAR = False

# show legal warning when starting the tool
# (default: True)
SHOW_WARNING = True


"""
RCE Module Configuration
"""
# Use a custom terminal emulator for the
# netcat listener. Use subprocess syntax and
# leave command value blank. (default: [])
TERMINAL = [

]

# How does the terminal accept commands?
# TERM -e "command -with args" --> "STRING"
# TERM -e command -with args --> "LIST"
# (default: "STRING" for konsole)
TERM_CMD_TYPE = "STRING"

# override the default payload used by the
# RCE module (reverse shell over /dev/tcp)
# if you want to spawn a reverse shell, use
# the placeholders <IP> and <PORT>
# (default: "")
PAYLOAD_OVERRIDE = ""
