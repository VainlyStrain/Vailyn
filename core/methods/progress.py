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

import sys
import shutil

from core.colors import color


def progress(iteration, total, prefix='', suffix='', decimals=1):
    """
    Call in a loop to create terminal progress bar
    @params:
        iteration   - Required  : current iteration (Int)
        total       - Required  : total iterations (Int)
        prefix      - Optional  : prefix string (Str)
        suffix      - Optional  : suffix string (Str)
        decimals    - Optional  : positive number of decimals in percent complete (Int)
    """
    percent = ("{0:." + str(decimals) + "f}").format(100 * (iteration / float(total)))
    if float(percent) > 100.0:
        percent = "100.0"
    erase()
    sys.stdout.write('%s %s%5s%%%s %s' % (prefix, color.RB, percent, color.END+color.RD+"|"+color.END, suffix))
    sys.stdout.flush()


def progressgui(iteration, total, dialog):
    """
    ATTENTION: ONLY CALL ME LOCKED !!!
    handle progressbar in GUI
    """
    percent = int(100 * (iteration / float(total)))
    if percent <= 100:
        dialog.progressBar.setValue(iteration)
        dialog.show()


def progresswin(iteration, total, prefix='', suffix='', decimals=1):
    """
    progress() alternative compatible with Windows
    """
    percent = ("{0:." + str(decimals) + "f}").format(100 * (iteration / float(total)))
    if float(percent) > 100.0:
        percent = "100.0"
    print("{}[VAILYN]{} {}{}%{} done.".format(color.RD, color.END, color.BOLD, percent, color.END))


def erase():
    """
    prevent progress() from flooding the terminal output
    """
    sys.stdout.write('\033[1K')
    if sys.platform.lower().startswith('win'):
        termwidth = shutil.get_terminal_size()[0]
        sys.stdout.write('\033[{}D'.format(termwidth))
    else:
        sys.stdout.write('\033[0G')
