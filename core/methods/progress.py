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

import sys, shutil

from core.colors import color


"""prints progress in percentage"""
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


"""
ATTENTION: ONLY CALL ME LOCKED !!!
handle progressbar in GUI
"""
def progressgui(iteration, total, dialog):
    percent = int(100 * (iteration / float(total)))
    if percent <= 100:
        dialog.progressBar.setValue(iteration)
        dialog.show()


"""progress() alternative compatible with Windows"""
def progresswin(iteration, total, prefix = '', suffix = '', decimals = 1):
    percent = ("{0:." + str(decimals) + "f}").format(100 * (iteration / float(total)))
    if float(percent) > 100.0:
        percent = "100.0"
    print("{}[VAILYN]{} {}{}%{} done.".format(color.RD, color.END, color.BOLD, percent, color.END))
    

"""prevent progress() from flooding the terminal output"""
def erase():
    sys.stdout.write('\033[1K')
    if sys.platform.lower().startswith('win'):
        termwidth = shutil.get_terminal_size()[0]
        sys.stdout.write('\033[{}D'.format(termwidth))
    else:
        sys.stdout.write('\033[0G')