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
       

┌─[pathtrav]─[~]
└──╼ VainlyStrain
"""

from core.methods.session import session
from http.cookies import SimpleCookie
import requests, sys
from core.colors import color
from core.variables import payloadlist, nullchars
from core.methods.filecheck import filecheck
from core.methods.loot import download



def getCookie(url):
    s = session()
    r = s.get(url)
    return s.cookies

def readCookie(url):
    #cookiestring = ""
    #with open(cookiefile, "r") as f:
    #    cookiestring = f.read().strip()
    #assert cookiestring != ""
    #scookie = SimpleCookie()
    #scookie.load(cookiestring)
    #make it compatible with requests
    cookie = getCookie(url)
    #for key, morsel in scookie.items():
    #    cookie[key] = morsel.value
    i = 0
    if len(cookie.keys()) < 1:
        sys.exit(color.R + "[-]" + color.END + " Server did not send any cookies.")
    for key in cookie.keys():
        print(str(i) + ": " + key)
        i += 1
    selected = input("\n[!] Select key for attack (int) :> ")
    selectedpart = list(cookie.keys())[int(selected)]
    #print(selectedpart)
    return (cookie, selectedpart)
