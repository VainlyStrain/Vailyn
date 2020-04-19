#!/usr/bin/env python
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
from core.variables import CLEAR_CMD
import subprocess

def banner():
    vaile = '''{0}                      |
                      :   
                      |   
                      .   
                      .   
                      .   
____, __             .|   
   + ;               .|   
   .{1}:,                       
     ’                      
    .              /      
    + ;           :,      
    ;.           /,       
   {0}  ;          /;' ;    
     ;         /;{2}|{0}  : ^  
     ’      / {2}:{0}  ;.’  °   
          '/; \\           
         ./ '. \\      {2}|{0}
          '.  ’·    __\\,_
         {1}   '.      {0}\\{1}`{2};{0}{1} 
              \\      {0}\\ {1}
              .\\.     {0}V{1}   
                \\.               
                 .,.      
                   .'.    
                  ''.;:     
                    .|.   
                     | .  
                     .    
                     {0}
    '''.format(color.END, color.BOLD, color.CURSIVE)
    subprocess.call(CLEAR_CMD)
    print(vaile)
