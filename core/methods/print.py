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
from core.variables import CLEAR_CMD
import subprocess, shutil, math, texttable
from core.methods.list import listsplit

def banner():
    vaile = '''{0}                      |
                      :   
                      |   
                      :   
                      . 
                      .
____, __              |   
   + ;               :|   
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

def listprint(plist):
    #tmplist = []
    print()
    for i in range(0, len(plist)):
        print("{0}{1:4}{2}|{3}  {4}".format(color.RB, i, color.END+color.RD, color.END, plist[i]))
    print("{0}{1}|{2}  {3}".format(color.RB, "   A"+color.END+color.RD, color.END, "ALL"))
        #tmpstr = "{0:4}  {1}".format(i, plist[i])
        #tmplist.append(tmpstr)
    #maxlen = len(max(tmplist, key=len))
    #termwidth = shutil.get_terminal_size()[0]
    #column_number = math.floor(termwidth/maxlen)
    #columns = listsplit(tmplist, column_number)
    #listdisplay(columns)
    print()

def listdisplay(gen):
    t = texttable.Texttable()
    headings = []
    t.header(headings)
    t.set_chars([" "," "," "," "])
    t.set_deco(texttable.Texttable.BORDER)
    listlist = []
    for l in gen:
      listlist.append(l)
    #for row in zip(*gen):
    #for row in zip(i for sub in gen for i in sub):
    for row in zip(*listlist):
        print(row)
        t.add_row(row)
    s = t.draw()
    print("\n" + s + "\n")