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

import requests, random
import core.variables as variables
from core.methods.tor import torcheck

"""
creates a new requests session for the attack
"""
def session():
    VaileSession = requests.session()
    VaileSession.proxies = {}
    #hide ominous requests user agent
    VaileSession.headers['User-agent'] = variables.user_agents[random.randrange(0, len(variables.user_agents))]
    #Tor support (as in Vaile/TIDoS)
    if variables.tor:
        VaileSession.proxies['http'] = 'socks5h://localhost:9050'
        VaileSession.proxies['https'] = 'socks5h://localhost:9050'
        torcheck()
    else:
        VaileSession.proxies['http'] = None
        VaileSession.proxies['https'] = None

    return VaileSession 

def random_ua(session):
    session.headers["User-agent"] = variables.user_agents[random.randrange(0, len(variables.user_agents))]
