#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import time

from http.cookiejar import MozillaCookieJar

def cookieFromFile(cookiefile):
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
