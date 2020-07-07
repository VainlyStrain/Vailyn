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

"""
This method filters out false positives. It does so by many different checks:
  + does the response match an initial ping?
  + are common error signatures in the response?
  + is the payload contained in the response? (indicating an error)
  + is the response empty? (some servers do not return 404, but 200 with empty response)
"""
def filecheck(r, con2, payload):
    con = r.content
    conn = str(con).lower()
    #prevents Vailyn to be stuck with long binary files (like zip archives)
    if r.encoding == None:
      r.encoding = "utf-8"
    txt = r.text.lower()
    check = (con != con2 and "[<a href='function.main'>function.main</a>" not in conn and "[<a href='function.include'>function.include</a>" not in conn 
    and ("failed opening" not in conn and "for inclusion" not in conn) and "failed to open stream:" not in conn and "open_basedir restriction in effect" not in conn 
    and payload.lower() not in txt and unquote(payload).lower() not in txt and "file_exists() expects parameter 1 to be a valid path" not in conn and conn != "b''")
    return check
