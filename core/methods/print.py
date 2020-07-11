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
import subprocess, shutil, math, sys, platform
from core.methods.list import listsplit
from core.variables import payloadlist

if platform.system() == 'Windows':
    from colorama.win32 import GetConsoleScreenBufferInfo, FillConsoleOutputCharacter, STDOUT

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

def listprint2(plist):
    print()
    for i in range(0, len(plist)):
        print("{0}{1:{5}}{2}|{3}  {4}".format(color.RB, i, color.END+color.RD, color.END, plist[i], len(str(len(payloadlist)))))
    print("{0}{1}|{2}  {3}".format(color.RB, "   A"+color.END+color.RD, color.END, "ALL"))
    print()

def listprint(plist):
    tmplist = []
    for i in range(0, len(plist)):
        #tmpstr = "{0:4}  {1}".format(i, plist[i])
        tmpstr = "{0}{1:{5}}{2}|{3}  {4}".format(color.RB, i, color.END+color.RD, color.END, plist[i], len(str(len(payloadlist))))
        tmplist.append(tmpstr)
    maxlen = len(max(tmplist, key=len))
    termwidth = shutil.get_terminal_size()[0]
    column_number = math.floor(len(plist)/(termwidth/((maxlen+4))))
    columns = listsplit(tmplist, column_number)
    listdisplay(columns, maxlen)

def listdisplay(gen, maxlen):
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
    print()

def progress (iteration, total, prefix = '', suffix = '', decimals = 1):
    """
    Call in a loop to create terminal progress bar
    @params:
        iteration   - Required  : current iteration (Int)
        total       - Required  : total iterations (Int)
        prefix      - Optional  : prefix string (Str)
        suffix      - Optional  : suffix string (Str)
        decimals    - Optional  : positive number of decimals in percent complete (Int)
        length      - Optional  : character length of bar (Int)
        fill        - Optional  : bar fill character (Str)
        printEnd    - Optional  : end character (e.g. "\r", "\r\n") (Str)
    """
    percent = ("{0:." + str(decimals) + "f}").format(100 * (iteration / float(total)))
    if float(percent) > 100.0:
        percent = "100.0"
    erase()
    sys.stdout.write('%s %s%5s%%%s %s' % (prefix, color.RB, percent, color.END+color.RD+"|"+color.END, suffix))
    sys.stdout.flush()
    

#this method stems from dirsearch
#(https://github.com/maurosoria/dirsearch) by Mauro Soria
def erase():
    if platform.system() == 'Windows':
        csbi = GetConsoleScreenBufferInfo()
        line = "\b" * int(csbi.dwCursorPosition.X)
        sys.stdout.write(line)
        width = csbi.dwCursorPosition.X
        csbi.dwCursorPosition.X = 0
        FillConsoleOutputCharacter(STDOUT, ' ', width, csbi.dwCursorPosition)
        sys.stdout.write(line)
        sys.stdout.flush()

    else:
        sys.stdout.write('\033[1K')
        sys.stdout.write('\033[0G')
