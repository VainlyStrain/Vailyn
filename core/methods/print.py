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


import subprocess
import shutil
import math
import random

from core.colors import color
from core.variables import CLEAR_CMD, payloadlist, rce
from core.methods.list import listsplit
from core.config import ASCII_ONLY


def banner():
    """
    prints asciiart when starting the tool
    """

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
    """.format(
        color.CURSIVE,
        color.END + color.RD,
        color.RD,
        color.END + color.O,
        color.END,
    )

    banners = [stealth]
    subprocess.run(CLEAR_CMD)

    if not ASCII_ONLY:
        print(banners[random.randrange(0, len(banners))])


"""
the following methods nicely output lists for payload selection
and result output
"""


def listprint2(plist, nullbytes, wrappers):
    pstr = ""
    for i in range(0, len(plist)):
        pstr = pstr + "{0}{1:{5}}{2}|{3}  {4}\n".format(
            "", i, "", "", plist[i], len(str(len(payloadlist)))
        )
    pstr = pstr + "{0}{1}|{2}  {3}\n".format("", "  A", "", "ALL")
    if nullbytes or wrappers:
        pstr = pstr + "{0}{1}|{2}  {3}\n".format("", "  N", "", "NONE")
    return pstr


def listprint(plist, nullbytes, wrappers):
    tmplist = []
    for i in range(0, len(plist)):
        tmpstr = "{0}{1:{5}}{2}|{3}  {4}".format(
            color.RB, i, color.END + color.RD, color.END,
            plist[i], len(str(len(payloadlist)))
        )
        tmplist.append(tmpstr)
    maxlen = len(max(tmplist, key=len))
    termwidth = shutil.get_terminal_size()[0]
    column_number = math.floor(len(plist) / (termwidth / ((maxlen + 4))))
    columns = listsplit(tmplist, column_number)
    listdisplay(columns, maxlen, nullbytes, wrappers)


def listdisplay(gen, maxlen, nb, wrappers):
    listlist = []
    for elem in gen:
        listlist.append(elem)
    maxlen2 = len(max(listlist, key=len))
    for sublist in listlist:
        while len(sublist) < maxlen2:
            sublist.append("")
    print()
    for row in zip(*listlist):
        tstr = ""
        for i in row:
            tstr = tstr + "{0:{1}}".format(i, maxlen) + "  "
        print(tstr)
    space = ""
    for i in range(0, len(str(len(payloadlist))) - 1):
        space += " "
    print("{0}{1}|{2}  {3}".format(
        color.RB,
        space + "A" + color.END + color.RD,
        color.END, "ALL"
    ))
    if nb or wrappers:
        print("{0}{1}|{2}  {3}".format(
            color.RB,
            space + "N" + color.END + color.RD,
            color.END, "NONE"
        ))
    print()


def table_print(oldTuple):
    newTuple = []
    for elem in oldTuple:
        newTuple.append("{}{}{}".format(color.END, elem, color.RD))
    return tuple(newTuple)


def table_entry_print(entry):
    formatted = []
    for payload in entry:
        formatted.append("{}{}{}".format(color.END, payload, color.RD))
    return ",\n".join(elem for elem in formatted)


def print_techniques_gui():
    tstr = ""
    items = rce.keys()
    for i in items:
        tstr = tstr + "{0}{1:{5}}{2}|{3}  {4}\n".format(
            "", i, "", "", rce[i], max(3, len(str(len(items)))),
        )
    tstr = tstr + "{0}{1}|{2}  {3}\n".format("", "  A", "", "ALL")
    return tstr


def print_techniques():
    tmplist = []
    items = rce.keys()
    for i in items:
        tmpstr = "{0}{1:{5}}{2}|{3}  {4}".format(
            color.RB, i, color.END + color.RD, color.END,
            rce[i], max(3, len(str(len(items)))),
        )
        tmplist.append(tmpstr)
    maxlen = len(max(tmplist, key=len))
    termwidth = shutil.get_terminal_size()[0]
    column_number = math.floor(len(items) / (termwidth / ((maxlen + 4))))
    columns = listsplit(tmplist, column_number)
    listdisplay(columns, maxlen, False, False)
