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


def filecheck(con, con2, payload):
    conn = str(con)
    check = (con != con2 and "[<a href='function.main'>function.main</a>" not in conn and "[<a href='function.include'>function.include</a>" not in conn 
    and ("Failed opening" not in conn and "for inclusion" not in conn) and "failed to open stream:" not in conn and "open_basedir restriction in effect" not in conn 
    and payload not in conn and "file_exists() expects parameter 1 to be a valid path" not in conn and conn != "b''" and "I see" not in conn)
    return check
