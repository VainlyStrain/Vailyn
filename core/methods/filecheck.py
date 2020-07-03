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

from urllib.parse import unquote

def filecheck(r, con2, payload):
    con = r.content
    conn = str(con).lower()
    txt = r.text.lower()
    check = (con != con2 and "[<a href='function.main'>function.main</a>" not in conn and "[<a href='function.include'>function.include</a>" not in conn 
    and ("failed opening" not in conn and "for inclusion" not in conn) and "failed to open stream:" not in conn and "open_basedir restriction in effect" not in conn 
    and payload.lower() not in txt and unquote(payload).lower() not in txt and "file_exists() expects parameter 1 to be a valid path" not in conn and conn != "b''")# and "I see" not in conn)
    #if check:
    #  print("=============\n"+payload+"\n--------\n"+txt+"\n============")
    return check
