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

import sys, os, time
import core.variables as variables
from core.methods.session import session
from core.colors import color

"""convert URL to directory name for cache"""
def parseUrl(url):
    baseurl = url.split("://")[1]
    name = baseurl.split("/")[0]
    if sys.platform.lower().startswith('win'):
        subdir = name+"\\"
    else:
        subdir = name+"/"
    return subdir

"""cache found payloads & nullbytes from phase 1"""
def save(subdir, plist, nlist):
    if not os.path.exists(variables.cachedir+subdir):
        os.makedirs(variables.cachedir+subdir)
    with open((variables.cachedir+subdir+"payloads.cache"), "w") as p:
        for i in plist:
            p.write(i+"\n")
    with open((variables.cachedir+subdir+"nullbytes.cache"), "w") as n:
        for i in nlist:
            n.write(i+"\n")

"""load payloads & nullbytes from cache"""
def load(subdir):
    plist = []
    nlist = []
    with open((variables.cachedir+subdir+"payloads.cache"), "r") as p:
        plist = p.read().splitlines()
    with open((variables.cachedir+subdir+"nullbytes.cache"), "r") as n:
        nlist = n.read().splitlines()
    return (plist, nlist)
