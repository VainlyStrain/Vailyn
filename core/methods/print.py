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

from core.colors import color
from core.variables import CLEAR_CMD
import subprocess, shutil, math, sys, random
from core.methods.list import listsplit
from core.variables import payloadlist, e_version


"""prints asciiart when starting the tool"""
def banner():
    large = '''{0}                      |
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
                     | '  
                     '    {0}
    '''.format(color.END, color.BOLD, color.CURSIVE)

    largemixed = '''{0}                      |
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
         ./ '. \\      
          '.  ’·  ; /_ '/ 
         {1}   '.    {0}|/(//((//) {1} 
              \\   {0}'     /  {1}
              .\\.      
                \\.               
                 .,.      
                   .'.    
                  ''.;:     
                    .|.   
                     | '  
                     '    {0}
    '''.format(color.END, color.BOLD, color.CURSIVE)
    
    mixed = '''{0}
    
    





    
    
____, __
   + ;  
   .{1}:,                       
     ’     ; /_ '/                   
    .      |/(//((//) {2}
    + ;    '     /  
    ;.           
   {0}  ;     
     ;      
     ’ {0}


     
    '''.format(color.END, color.BOLD, color.END + color.CURSIVE + e_version + color.END + color.BOLD)
    
    small1 = '''; /_ '/    
|/(//((//) 
'     /   

    '''
    
    small2 = '''| /  .|  ,_
|/ (|||\\/||
'      /  

    '''

    medium1 = ''' __  _, ___,   ____, __    __  _, ____,  
  \\ |  (-|_\\_,(-|   (-|   (-\\ |  (-|  |  
   \\|   _|  )  _|__, _|__,   \\|   _|  |_,
    '  (      (     (      (__/  (       
    
    '''
    
    medium2 = ''' __  _,_    ___, ,    ,  ,  , 
  \\ |  |\\  ' |   |    \\_/|\\ | 
   \\|  |-\\  _|_,'|__ , /`|'\\| 
    '  '  `'       '(_/  '  `
    
    '''
    
    #banners = [large, large, large, medium1, medium2, small1, small2, mixed, mixed, mixed]
    banners = [large, largemixed]
    
    subprocess.run(CLEAR_CMD)
    print(banners[random.randrange(0, len(banners))])

"""
the following methods nicely output lists for the payload selection

currently in use: listprint
"""

def listprint2(plist, nullbytes):
    pstr = ""
    for i in range(0, len(plist)):
        pstr = pstr + "{0}{1:{5}}{2}|{3}  {4}\n".format("", i, "", "", plist[i], len(str(len(payloadlist))))
    pstr = pstr + "{0}{1}|{2}  {3}\n".format("", "  A", "", "ALL")
    if nullbytes:
        pstr = pstr + "{0}{1}|{2}  {3}\n".format("", "  N", "", "NONE")
    return pstr

def listprint(plist, nullbytes):
    tmplist = []
    for i in range(0, len(plist)):
        #tmpstr = "{0:4}  {1}".format(i, plist[i])
        tmpstr = "{0}{1:{5}}{2}|{3}  {4}".format(color.RB, i, color.END+color.RD, color.END, plist[i], len(str(len(payloadlist))))
        tmplist.append(tmpstr)
    maxlen = len(max(tmplist, key=len))
    termwidth = shutil.get_terminal_size()[0]
    column_number = math.floor(len(plist)/(termwidth/((maxlen+4))))
    columns = listsplit(tmplist, column_number)
    listdisplay(columns, maxlen, nullbytes)

def listdisplay(gen, maxlen, nb):
    listlist = []
    for l in gen:
      listlist.append(l)
    maxlen2 = len(max(listlist, key=len))
    for l in listlist:
        while len(l) < maxlen2:
            l.append("")
    print()
    for row in zip(*listlist):
        tstr = ""
        for i in row:
            tstr = tstr + "{0:{1}}".format(i, maxlen) + "  "
        print(tstr)
    space = ""
    for i in range(0, len(str(len(payloadlist)))-1):
        space += " "
    print("{0}{1}|{2}  {3}".format(color.RB, space+"A"+color.END+color.RD, color.END, "ALL"))
    if nb:
        print("{0}{1}|{2}  {3}".format(color.RB, space+"N"+color.END+color.RD, color.END, "NONE"))
    print()

