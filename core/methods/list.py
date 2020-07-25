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


"""equally split list for threads"""
def listsplit(l, n):
    if n == 0:
        n += 1
    for i in range(0, len(l), n):
        yield l[i:i + n]  
