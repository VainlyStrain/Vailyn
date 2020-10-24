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

from http.cookiejar import FileCookieJar

from core.colors import color
from core.variables import timeout
from core.methods.session import session


def getCookie(url):
    """
    fetches cookies from the website for the cookie attack
    @params:
        url - URL to fetch cookies from.
    """
    s = session()
    try:
        s.get(url, timeout=timeout)
    except (requests.exceptions.Timeout, requests.exceptions.ConnectionError):
        sys.exit("Timeout fetching cookie.")
    return s.cookies


def readCookie(url):
    """
    parses cookies and lets the attacker choose the injedction point
    @params:
        url - URL to fetch cookies from.
    """
    cookie = getCookie(url)
    i = 0
    if len(cookie.keys()) < 1:
        sys.exit(color.R + "[-]" + color.END + " Server did not send any cookies.")
    for key in cookie.keys():
        print(str(i) + ": " + key)
        i += 1
    selected = input("\n[!] Select key for attack (int) :> ")
    selectedpart = list(cookie.keys())[int(selected)]
    return (cookie, selectedpart)


def cookieFromFile(cookiefile):
    """
    reads authentication cookie from file
    @params:
        cookiefile - File containing the cookies.
    """
    jar = FileCookieJar('cookiefile')
    jar.load(ignore_expires=True)
    # set expiration time to avoid errors
    for cookie in jar:
        cookie.expires = time.time() + 14 * 24 * 3600
    assert(len(jar) > 0)
    return jar
