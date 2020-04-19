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

import sys, os
import core.variables as variables
from core.session import session
from core.colors import color


def download(url, file):
    requests = session()
    if sys.platform.lower().startswith('win'):
        if "\\" in file:
            path ='\\'.join(file.split('\\')[0:-1])
            baseurl = url.split("://")[1]
            name = baseurl.split("\\")[0]
        else:
            path ='\\'.join(file.split('/')[0:-1])
            baseurl = url.split("://")[1]
            name = baseurl.split("/")[0]
        subdir = name+"\\"
    else:
        if "\\" in file:
            path ='/'.join(file.split('\\')[0:-1])
            baseurl = url.split("://")[1]
            name = baseurl.split("\\")[0]
        else:
            path ='/'.join(file.split('/')[0:-1])
            baseurl = url.split("://")[1]
            name = baseurl.split("/")[0]
        subdir = name+"/"
    if not os.path.exists(variables.lootdir+subdir+path):
        os.makedirs(variables.lootdir+subdir+path)
    with open((variables.lootdir+subdir+file), "wb") as loot:
        response = requests.get(url)
        loot.write(response.content)
    loot.close()
    print('{}[LOOT]{} {}'.format(color.RD, color.END+color.O+color.BOLD, file+color.END))
