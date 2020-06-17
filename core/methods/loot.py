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

import sys, os, time
import core.variables as variables
from core.methods.session import session
from core.colors import color

date = time.strftime("%Y-%m-%d %H:%M:%S")

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
        subdir = name+"-"+str(date)+"\\"
    else:
        if "\\" in file:
            path ='/'.join(file.split('\\')[0:-1])
            baseurl = url.split("://")[1]
            name = baseurl.split("\\")[0]
        else:
            path ='/'.join(file.split('/')[0:-1])
            baseurl = url.split("://")[1]
            name = baseurl.split("/")[0]
        subdir = name+"-"+str(date)+"/"
    if not os.path.exists(variables.lootdir+subdir+path):
        os.makedirs(variables.lootdir+subdir+path)
    with open((variables.lootdir+subdir+file), "wb") as loot:
        response = requests.get(url)
        loot.write(response.content)
    loot.close()
    print('{}[LOOT]{} {}'.format(color.RD, color.END+color.O+color.CURSIVE, file+color.END))
