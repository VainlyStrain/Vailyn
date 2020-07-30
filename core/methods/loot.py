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

#append date to folder to be unique
if sys.platform.lower().startswith('win'):
    date = time.strftime("%Y-%m-%d %H-%M-%S")
else:
    date = time.strftime("%Y-%m-%d %H:%M:%S")

"""download found files & save them in the loot folder"""
def download(url, file, cookie=None, post=None):
    requests = session()
    if cookie:
        requests.cookies = cookie
    if sys.platform.lower().startswith('win'):
        if "\\" in file:
            path ='\\'.join(file.split('\\')[0:-1])
            baseurl = url.split("://")[1]
            name = baseurl.split("\\")[0]
        else:
            path ='\\'.join(file.split('/')[0:-1])
            baseurl = url.split("://")[1]
            name = baseurl.split("/")[0]

        #fixes directory issues on Windows, because it doesn't allow the character :, which is used in URIs
        if "@" in name:
            name = name.split("@")[1]
        name = name.split(":")[0]
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

        if "@" in name:
            name = name.split("@")[1]
        name = name.split(":")[0]
        subdir = name+"-"+str(date)+"/"
    if not os.path.exists(variables.lootdir+subdir+path):
        os.makedirs(variables.lootdir+subdir+path)
    with open((variables.lootdir+subdir+file), "wb") as loot:
        if not post:
            response = requests.get(url)
        else:
            response = requests.post(url, data=post)
        loot.write(response.content)
    loot.close()
    print('{}[LOOT]{} {}'.format(color.RD, color.END+color.O+color.CURSIVE, file+color.END))
