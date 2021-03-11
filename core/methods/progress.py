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

from core.colors import color, lines
from core.variables import is_windows


def progress(iteration, total, prefix="", suffix="", decimals=1):
    """
    Call in a loop to create terminal progress bar
    @params:
        iteration   - current iteration (Int)
        total       - total iterations (Int)
        prefix      - prefix string (Str)
        suffix      - suffix string (Str)
        decimals    - number of decimals in percent complete (Int)
    """
    percent = ("{0:." + str(decimals) + "f}").format(
        100 * (iteration / float(total)),
    )
    if float(percent) > 100.0:
        percent = "100.0"
    erase()
    sys.stdout.write("%s %s%5s%%%s %s" % (
        prefix, color.RB, percent,
        color.END + color.RD + lines.VL + color.END,
        suffix,
    ))
    sys.stdout.flush()


def progress_gui(iteration, total, dialog):
    """
    ATTENTION: ONLY CALL ME LOCKED !!!
    handle progressbar in GUI
    """
    percent = int(100 * (iteration / float(total)))
    if percent <= 100:
        dialog.progressBar.setValue(iteration)
        dialog.show()


def progress_win(iteration, total, prefix="", suffix="", decimals=1):
    """
    progress() alternative compatible with Windows
    """
    percent = ("{0:." + str(decimals) + "f}").format(
        100 * (iteration / float(total)),
    )
    if float(percent) > 100.0:
        percent = "100.0"
    print("{}[VAILYN]{} {}{}%{} done.".format(
        color.RD, color.END, color.BOLD, percent, color.END,
    ))


def erase():
    """
    prevent progress() from flooding the terminal output
    """
    sys.stdout.write("\033[1K")
    if is_windows:
        termwidth = shutil.get_terminal_size()[0]
        sys.stdout.write("\033[{}D".format(termwidth))
    else:
        sys.stdout.write("\033[0G")
