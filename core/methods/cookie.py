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


import requests
import sys

from core.colors import color
from core.variables import timeout
from core.methods.session import session


def fetch_cookie(url, auth_cookie=""):
    """
    fetches cookies from the website for the cookie attack
    @params:
        url - URL to fetch cookies from.
    """
    s = session()
    if auth_cookie:
        requests.utils.add_dict_to_cookiejar(
            s.cookies,
            dict_from_header(auth_cookie),
        )
    try:
        s.get(url, timeout=timeout)
    except (
        requests.exceptions.Timeout,
        requests.exceptions.ConnectionError,
    ):
        sys.exit("Timeout fetching cookie.")
    return s.cookies


def read_cookie(url, auth_cookie=""):
    """
    parses cookies and lets the attacker choose the
    injection point

    @params:
        url - URL to fetch cookies from.
    """
    cookie = fetch_cookie(url, auth_cookie=auth_cookie)
    i = 0
    if len(cookie.keys()) < 1:
        sys.exit(
            color.R + "[-]" + color.END
            + " Server did not send any cookies."
        )
    for key in cookie.keys():
        print(str(i) + ": " + key)
        i += 1
    selected = input("\n[!] Select key for attack (int) :> ")
    selected_part = list(cookie.keys())[int(selected)]
    return (cookie, selected_part)


def dict_from_header(header):
    """
    converts a cookie header to a dictionary
    """
    # FIXME: breaks with base64 encoded cookies
    result = {}
    cookies = header.split(";")
    for cookie in cookies:
        parsed = cookie.strip().split("=")
        result[parsed[0].strip()] = parsed[1].strip()
    return result


def jar_from_dict(cookiedict):
    """
    converts a dictionary to a cookiejar
    """
    return requests.utils.cookiejar_from_dict(cookiedict)
