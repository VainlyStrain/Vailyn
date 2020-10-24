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

import sys
import os

import core.variables as variables


def parseUrl(url):
    """
    convert URL to directory name for cache
    @params:
        url - URL to convert.
    """
    baseurl = url.split("://")[1]
    name = baseurl.split("/")[0]

    # patch for Windows, which does not allow certain URI chars in dirname
    if "@" in name:
        name = name.split("@")[1]
    name = name.split(":")[0]
    if sys.platform.lower().startswith('win'):
        subdir = name+"\\"
    else:
        subdir = name+"/"
    return subdir


def save(subdir, plist, nlist):
    """
    cache found payloads & nullbytes from phase 1
    @params:
        subdir - cache directory name
        plist  - list of found payloads
        nlist  - list of found nullbytes
    """
    if not os.path.exists(variables.cachedir + subdir):
        os.makedirs(variables.cachedir + subdir)
    with open((variables.cachedir + subdir + "payloads.cache"), "w") as p:
        for i in plist:
            p.write(i + "\n")
    with open((variables.cachedir+subdir+"nullbytes.cache"), "w") as n:
        for i in nlist:
            n.write(i + "\n")


def load(subdir):
    """
    load payloads & nullbytes from cache
    @params:
        subdir - cache directory name.
    """
    plist = []
    nlist = []
    with open((variables.cachedir + subdir + "payloads.cache"), "r") as p:
        plist = p.read().splitlines()
    with open((variables.cachedir + subdir + "nullbytes.cache"), "r") as n:
        nlist = n.read().splitlines()
    return (plist, nlist)
