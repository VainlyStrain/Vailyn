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
from core.methods.print import listprint

"""
select specific payloads or nullbytes for phase 2
@payloadlist: payloads or nullbytes found in phase 1
"""
def select(payloadlist, nullbytes=False):
    #filter duplicates
    payloadlist = list(set(payloadlist))
    if nullbytes:
        #print("\n{0}[+]{1} Operative nullbytes ({2}{3}{1}):\n {4}".format(color.RD, color.END, color.BOLD, len(payloadlist), str(payloadlist)))
        print("\n{0}[+]{1} Operative nullbytes ({2}{3}{1}):".format(color.RD, color.END, color.BOLD, len(payloadlist)))
    else:
        #print("\n{0}[+]{1} Operative payloads ({2}{3}{1}):\n {4}".format(color.RD, color.END, color.BOLD, len(payloadlist), str(payloadlist)))
        print("\n{0}[+]{1} Operative payloads ({2}{3}{1}):".format(color.RD, color.END, color.BOLD, len(payloadlist)))
    #print(color.BOLD+"\n  Operative Payloads:\n"+color.END+" "+color.O+str(payloadlist)+color.END)
    listprint(payloadlist)
    invalid = True
    while invalid:
        if nullbytes:
            payloads = input("Select nullbyte indexes for the attack (comma-separated) :> ")
        else:
            payloads = input("Select payload indexes for the attack (comma-separated) :> ")
        try:
            if payloads.strip().lower() == "a":
                return payloadlist
            selected = [payloadlist[int(i.strip())] for i in payloads.split(",")]
            invalid = False
        except:
            pass
    return selected
