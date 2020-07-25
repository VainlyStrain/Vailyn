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

"""
creates a new requests session for the attack
"""
def session():
    VaileSession = requests.session()
    VaileSession.proxies = {}
    #hide ominous requests user agent
    VaileSession.headers['User-agent'] = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.79 Safari/537.36 Edge/14.14393'
    #TODO Tor support (as in Vaile/TIDoS)
    '''
    if vars.tor:
        VaileSession.proxies['http'] = 'socks5h://localhost:9050'
        VaileSession.proxies['https'] = 'socks5h://localhost:9050'
        torcheck()
    else:
        VaileSession.proxies['http'] = None
        VaileSession.proxies['https'] = None
    '''
    return VaileSession 
