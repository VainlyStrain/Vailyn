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

from core.colors import color

def select(payloadlist):
    #filter duplicates
    payloadlist = list(set(payloadlist))
    print(color.BOLD+"\n  Operative Payloads:\n"+color.END+" "+color.O+str(payloadlist)+color.END)
    invalid = True
    while invalid:
        payloads = input("Select payloads indexes for the attack (comma-separated) :> ")
        try:
            selected = [payloadlist[int(i.strip())] for i in payloads.split(",")]
            invalid = False
        except:
            pass
    return selected
