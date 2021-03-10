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
import time
import requests

import core.variables as variables

from urllib.parse import unquote

from core.colors import color
from core.variables import SEPARATOR, is_windows


date = ""


def set_date():
    global date
    # append date to folder to be unique
    if is_windows:
        date = time.strftime("%Y-%m-%d %H-%M-%S")
    else:
        date = time.strftime("%Y-%m-%d %H:%M:%S")


def download(url, file, attack, s, cookie=None, post=None):
    """
    download found files & save them in the loot folder
    @params:
        url    - URL to be downloaded from.
        file   - file name. (with path)
        cookie - cookie to be used.
        post   - should we do a POST request? (default: GET)
    """

    url_separator = "/"
    if "\\" in file:
        url_separator = "\\"

    path = SEPARATOR.join(file.split(url_separator)[0:-1])
    base_url = url.split("://")[1]
    name = base_url.split(url_separator)[0]

    # fixes directory issues on Windows, because it doesn't
    # allow the character :, which is used in URIs
    if "@" in name:
        name = name.split("@")[1]
    name = name.split(":")[0]
    subdir = name + "-" + str(date) + SEPARATOR

    if not os.path.exists(variables.lootdir + subdir + path):
        os.makedirs(variables.lootdir + subdir + path)
    with open((variables.lootdir + subdir + file), "wb") as loot:
        if not post:
            try:
                response = s.get(url, timeout=variables.timeout)
            except (
                requests.exceptions.Timeout,
                requests.exceptions.ConnectionError,
            ):
                print("Timeout reached looting " + url)
                return
        else:
            try:
                if attack == 4:
                    req = requests.Request(method="POST", url=url, data=post)
                    prep = s.prepare_request(req)
                    new_body = unquote(prep.body)
                    prep.body = new_body
                    prep.headers["content-length"] = len(new_body)
                    response = s.send(prep, timeout=variables.timeout)
                elif attack == 5:
                    req = requests.Request(method="POST", url=url, json=post)
                    prep = s.prepare_request(req)
                    new_body = unquote(prep.body)
                    prep.body = new_body
                    prep.headers["content-length"] = len(new_body)
                    response = s.send(prep, timeout=variables.timeout)
            except (
                requests.exceptions.Timeout,
                requests.exceptions.ConnectionError,
            ):
                print("Timeout reached looting " + url)
                return
        loot.write(response.content)
    loot.close()
    print("{}[LOOT]{} {}".format(
        color.RD,
        color.END + color.RB + color.CURSIVE,
        file + color.END
    ))
