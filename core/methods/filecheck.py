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


import core.variables as variables

import re

from urllib.parse import unquote


def filecheck(r, con2, con3, payload, post=False):
    """
    This method filters out false positives.
    It does so by many different checks, listed in the
    README.md file.
    """
    con = r.content
    conn = str(con).lower()

    # /etc/passwd regex to reduce false positives
    # in default configuration
    passwd_regex = "\w*:\w*:[0-9]*:[0-9]*:\w*:"

    if variables.lfi:
        for wrapper in variables.phase1_wrappers:
            payload = payload.replace(wrapper, "")

    try:
        # false positive prevention in case server has default include
        # which disappears in case of file not found
        conb2 = con2.decode().lower().strip()
        conb = con.decode().lower().strip()
        check2 = conb not in conb2
    except Exception:
        """
        if we get an encoding error, it may mean 2 things:
          a) we just successfully included a binary file --> vulnerable
          b) it happened all the time, so return true to prevent false
             negatives
        """
        check2 = True
    # prevents Vailyn to be stuck with long binary files
    # (like zip archives)
    if r.encoding is None:
        r.encoding = "utf-8"

    txt = r.text.lower()
    check = (
        con != con2
        and "[<a href='function.main'>function.main</a>" not in conn
        and "[<a href='function.include'>function.include</a>" not in conn
        and ("failed opening" not in conn and "for inclusion" not in conn)
        and "failed to open stream:" not in conn
        and "open_basedir restriction in effect" not in conn
        and payload.lower() not in txt
        and unquote(payload).lower() not in txt
        and "file_exists() expects parameter 1 to be a valid path" not in conn
        and conn != "b''"
        and check2
    )

    # does attack page match /etc/passwd, and does it really
    # come from our inclusion/traversal?
    reg_check = (
        re.findall(passwd_regex, txt)
        and not re.findall(passwd_regex, str(con2).lower())
    )

    if con3:
        check = check and con3 != con
        reg_check = (
            reg_check
            and not re.findall(passwd_regex, str(con3).lower())
        )

    if "etc/passwd" in payload:
        check = check and reg_check

    return check
