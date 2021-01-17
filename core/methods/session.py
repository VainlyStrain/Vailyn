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
import random
import core.variables as variables
from core.methods.tor import tor_check


def session():
    """
    creates a new requests session for the attack
    """
    VailynSession = requests.session()
    VailynSession.proxies = {}
    # hide ominous requests user agent
    VailynSession.headers["User-agent"] = variables.user_agents[
        random.randrange(0, len(variables.user_agents))
    ]
    # Tor support (as in Vaile/TIDoS)
    if variables.tor:
        VailynSession.proxies["http"] = "socks5h://localhost:9050"
        VailynSession.proxies["https"] = "socks5h://localhost:9050"
        tor_check()
    else:
        VailynSession.proxies["http"] = None
        VailynSession.proxies["https"] = None

    return VailynSession


def random_ua(session):
    """
    select and apply a random useragent
    """
    session.headers["User-agent"] = variables.user_agents[
        random.randrange(0, len(variables.user_agents))
    ]
