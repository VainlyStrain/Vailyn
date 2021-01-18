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


from core.methods.session import session
from core.variables import e_version


def check_version():
    """
    compare local version with online version
    """
    try:
        s = session()
        onver = s.get(
            "https://raw.githubusercontent.com/VainlyStrain"
            "/Vailyn/master/core/doc/VERSION",
            timeout=2,
        ).text.strip()

        localmain = e_version.split("-")[0]
        localrev = e_version.split("-")[1]
        locallist = localmain.split(".")
        onmain = onver.split("-")[0]
        onrev = onver.split("-")[1]
        onlist = onmain.split(".")
        uptodate = True
        matches = True
        for i in range(0, len(locallist)):
            if int(locallist[i]) < int(onlist[i]):
                uptodate = False
        for i in range(0, len(locallist)):
            if int(locallist[i]) != int(onlist[i]):
                matches = False
        if uptodate and matches:
            if int(localrev) < int(onrev):
                uptodate = False
        return uptodate
    except Exception:
        return True
