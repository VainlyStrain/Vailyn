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
import time

from http.cookiejar import MozillaCookieJar

from core.colors import color
from core.variables import timeout
from core.methods.session import session


def fetch_cookie(url):
    """
    fetches cookies from the website for the cookie attack
    @params:
        url - URL to fetch cookies from.
    """
    s = session()
    try:
        s.get(url, timeout=timeout)
    except (
        requests.exceptions.Timeout,
        requests.exceptions.ConnectionError,
    ):
        sys.exit("Timeout fetching cookie.")
    return s.cookies


def read_cookie(url):
    """
    parses cookies and lets the attacker choose the
    injection point

    @params:
        url - URL to fetch cookies from.
    """
    cookie = fetch_cookie(url)
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


def cookie_from_file(cookiefile):
    """
    reads authentication cookie from file
    @params:
        cookiefile - File containing the cookies.
    """
    jar = MozillaCookieJar(cookiefile)
    jar.load(ignore_expires=True)
    # set expiration time to avoid errors
    for cookie in jar:
        cookie.expires = time.time() + 14 * 24 * 3600
    assert(len(jar) > 0)
    return jar
