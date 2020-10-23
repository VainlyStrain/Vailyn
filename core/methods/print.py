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
    
    largedark = '''{0}                      |
                      :   
                      |   
                      :   
                      . 
                      .
____{4},{0} __              |   
   {4}+{0}{1} {4};{0}               :|   
   {4}.{1}:,{0}{1}                       
     {4}’{0}{1}                      
    {4}.{0}{1}              /      
    {4}+{0}{1} {4};{0}{1}           :,      
    {4};.{0}{1}           /,       
   {0}  {4};{0}          /;' ;    
     {4};{0}         /;{2}|{0}  : ^  
     {4}’{0}      / {2}:{0}  ;.’  °   
          '/; \\           
         ./ '. \\      
          '.  ’·   {0}
         {1}   '.    {0}|{3} Vailyn {0}|{1}
               {0}[ {6}VainlyStrain{0} ]{0}{1}
               ,     
                \\.               
                 .,.      
                   .'.    
                  ''.;:     
                    .|.   
                     | '  
                     '    {5}
    '''.format(color.END + color.RD, color.BOLD, color.CURSIVE, color.END+color.O, color.RD, color.END, color.END+color.R)
    
    stealth = """{1}
   ,                \\                  /      {0}         , {1}
     ':.             \\.      /\\.     ./   {0}         .:'      
        ':;.          {1}:\\ .,:/   ''. /;  {0}      ..::'        
           ',':.,.__.'' '          ' `:.__:''.:'            
              ';..                {1}        ,;'     {2}*{1}{0}        
       {2}*{1}         '.,                  {0} .:'                  
                    `v;.            ;v'        {2}o{1}{0}      
              {2}.{1}      '  '.{1}.      :.' '     {2}.{1}                  
                     '     ':;, '    '                       
            {2}o{1}                '          {2}.   :{1}        {1}
                                           {2}*{1}
                         |{3} Vailyn {1}|
                      [ VainlyStrain ]{4}
    """.format(color.CURSIVE, color.END + color.RD, color.RD, color.END + color.O, color.END)

    bold = """
            '  ___°         O  ‚  ’ ____                      ‘  ____‚            
_____.  '   ‚ /¯¯¯/|__„   ____   |\\¯¯¯¯\\ °               ____ ‘ |\\¯¯¯¯\\  ____  
 `\\¯¯\\   ___‚/ ' /\\¯¯¯\\°|\\¯¯¯¯\\°'\\| ' |‚‚        ____  |¯¯¯¯'|‘'\\|    \\|¯¯¯¯| 
 : \\  \\'/|¯¯¯||' |_|,  |‚ \\| ' |'/    /|   ____‚ |¯¯¯¯'|\\| '  |‘'/   '/\\ '°  |°
  \\:\\  \\/___/||  |¯|'  |‚‚/ ' /||    |/  /¯¯¯¯/|‚|\\____\\| '   | |  ' | \\|____|°
   \\:\\___\\¯|/‘|' |¯| ' |‚|  ' |/”|\\____\\/    /'/°'\\|'¯¯|    ' | |\\____\\ |¯ ¯ |‚’
   '\\|¯ ¯|¯¯' |\\__\\|°  |‚|\\____\\°'\\|¯'¯¯/____/;/‚   ¯¯¯¯/____/| '\\|¯¯ |  ¯¯¯¯’ 
     ¯¯¯'    ‘\\|¯ |/___/|‚'\\|¯¯|    ¯¯¯|'¯'¯ |/‚       |¯ ¯|/‘    ¯¯¯¯’          
            '   ¯¯|¯¯¯|/”   ¯¯¯¯        ¯¯¯¯”          ¯¯¯¯‘             ‘         
            '      ¯¯¯°                                           ‘                      
  
    """

    bold2 = """
_____.,   ____       ____      ____      ____        ___    ___     ____    ____
 `\\¯¯¯\\ '/¯¯¯/|    '|\\¯¯¯\\ °  |\\¯¯¯\\‚   |\\¯¯¯\\‘     |¯¯¯|  |¯¯¯|° '/¯¯¯¯|  /¯¯¯¯|  
 :'\\   \\/   /'| '/¯¯¯/\\   \\   | |  |'   | |  | '    |\\   \\°|   |° |     '\\'|   /|‘ 
 '\\ \\ '    / /' |  '|_|  °|'‚°'\\|  |'  '°\\|  |___¸  |.\\__¸\\|   |' |\\   |\\ \\|   |'|°
   \\ \\   '/ /   |  '|¯|  °|'‚ '°|   |'  '°|      '| °|¯¯¯| |   |‘ |'| °|  \\    °|/  
    \\'\\_¸/ /'   |\\___\\_\\___\\‚  '|\\__¸\\'  /________|  |\\___\\|___| ''/___|\\ /____¸|°  
    '\\| '|/     | |   | |   |  '| |   |'°|        '| | |  ||   | '|    |'\\|     |   
     '|__|'    °'\\|___|°|__¸¸'| °\\|__¸|'°|________'| '\\|__||__¸| '|__¸'| '|____''|    
 

    """

    #banners = [large, large, large, medium1, medium2, small1, small2, mixed, mixed, mixed]
    banners = [large, largemixed, bold, bold2, stealth, largedark, largedark, largedark]
    
    subprocess.run(CLEAR_CMD)
    print(banners[random.randrange(0, len(banners))])
    #print(largedark)

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
        tmpstr = "{0}{1:{5}}{2}|{3}  {4}".format(color.RB, i, color.END+color.RD, color.END, 
        plist[i], len(str(len(payloadlist))))
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

