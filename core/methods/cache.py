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


def parse_url(url):
    """
    convert URL to directory name for cache
    @params:
        url - URL to convert.
    """
    base_url = url.split("://")[1]
    name = base_url.split("/")[0]

    # patch for Windows, which does not allow certain URI
    # chars in dirname
    if "@" in name:
        name = name.split("@")[1]
    name = name.split(":")[0]
    if variables.is_windows:
        subdir = name + "\\"
    else:
        subdir = name + "/"
    return subdir


def save(subdir, plist, nlist, wlist):
    """
    cache found payloads & nullbytes from phase 1
    @params:
        subdir - cache directory name
        plist  - list of found payloads
        nlist  - list of found nullbytes
        wlist  - list of found PHP wrappers
    """
    if not os.path.exists(variables.cachedir + subdir):
        os.makedirs(variables.cachedir + subdir)

    with open(
        (variables.cachedir + subdir + "payloads.cache"),
        "w",
    ) as pcache:
        for payload in plist:
            pcache.write(payload + "\n")

    with open(
        (variables.cachedir + subdir + "nullbytes.cache"),
        "w",
    ) as ncache:
        for nullbyte in nlist:
            ncache.write(nullbyte + "\n")

    with open(
        (variables.cachedir + subdir + "wrappers.cache"),
        "w",
    ) as wcache:
        for wrapper in wlist:
            wcache.write(wrapper + "\n")


def load(subdir):
    """
    load payloads & nullbytes from cache
    @params:
        subdir - cache directory name.
    """
    plist = []
    nlist = []
    wlist = []
    with open(
        (variables.cachedir + subdir + "payloads.cache"),
        "r",
    ) as pcache:
        plist = pcache.read().splitlines()

    with open(
        (variables.cachedir + subdir + "nullbytes.cache"),
        "r",
    ) as ncache:
        nlist = ncache.read().splitlines()

    with open(
        (variables.cachedir + subdir + "wrappers.cache"),
        "r",
    ) as wcache:
        wlist = wcache.read().splitlines()

    return (plist, nlist, wlist)
