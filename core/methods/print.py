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

from terminaltables import SingleTable, AsciiTable

from core.colors import color, lines, INFO, ENUM, TRI
from core.variables import CLEAR_CMD, payloadlist, rce, vector_dict
from core.methods.list import listsplit
from core.config import ASCII_ONLY, NO_CLEAR, SHOW_WARNING


def intro(shell=False):
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
                         {5}{3} Vailyn {1}{5}
                      [ VainlyStrain ]{4}
    """.format(
        color.CURSIVE,
        color.END + color.RD,
        color.RD,
        color.END + color.RB,
        color.END,
        lines.VL,
    )

    shell_inf = """ {3}{0}{0}{0}{2} {4} Vailyn Interactive Shell  {2}{3}{5}{2}
 {3}{0}{0}{0}{2} {4} {1}?{2}{4} for help and {1}q{2}{4} to close {2}{3}{5}{2}
    """.format(
        INFO, color.BOLD, color.END, color.RFD,
        color.CURSIVE + color.RB, lines.VL,
    )

    banners = [stealth]
    if not NO_CLEAR and not shell:
        subprocess.run(CLEAR_CMD)

    if shell:
        print(shell_inf)
    elif not ASCII_ONLY:
        print(banners[random.randrange(0, len(banners))])


def help_formatter(
    cmd, msg, args={}, syntax="", examples=[], further=[],
):
    """
    formats the help message for the interactive shell.
    """
    DATA = []
    for line in msg.split("\n"):
        line = line.strip()
        if line:
            DATA.append(table_print([line]))
    if ASCII_ONLY:
        table = AsciiTable(DATA, "[ {0}{2}{1} ]".format(
            color.END + color.BOLD,
            color.END + color.RD,
            cmd,
        ))
    else:
        table = SingleTable(DATA, "[ {0}{2}{1} ]".format(
            color.END + color.BOLD,
            color.END + color.RD,
            cmd,
        ))
    table.inner_heading_row_border = False
    print("\n" + color.RD + table.table)
    # print("\n{0} -- {1}{2}{0} --\n".format(
    #     color.END, color.BOLD, cmd,
    # ))
    # for line in msg.split("\n"):
    #     print("  " + line)
    if args:
        print("{0}\n  ::  {1}Command Syntax{0}  ::".format(
            color.END, color.BOLD,
        ))
        if syntax:
            formatted = syntax_formatter(syntax.split(" "))
            print("\n  {}".format(formatted))
        dict_formatter(args)
    if examples:
        print("{0}\n  ::  {1}Examples{0}  ::".format(
            color.END, color.BOLD,
        ))
        list_formatter(examples)
    if further:
        print("{0}\n  ::  {1}See Also{0}  ::".format(
            color.END, color.BOLD,
        ))
        list_formatter(further)
    if not (args or examples or further):
        print()


def syntax_formatter(splitted):
    """
    Formats command syntax strings for the shell help
    menu.
    """
    result = color.RBB + splitted[0] + color.END + color.RB
    for i in range(1, len(splitted)):
        result = result + " " + splitted[i]
    result = result + TRI + color.END
    return result


def list_formatter(outlist):
    """
    Formats lists for display in the shell.
    """
    for elem in outlist:
        print("{0}   {1} {2}".format(color.END, ENUM, elem))
    print()


def list_formatter_columns(inlist, space=True):
    """
    Formats lists in columns in the shell.
    """
    tmplist = []
    for elem in inlist:
        tmpstr = "{0}    {1} {2}".format(
            color.END, ENUM, elem,
        )
        tmplist.append(tmpstr)
    maxlen = len(max(tmplist, key=len))
    termwidth = shutil.get_terminal_size()[0]
    column_number = math.floor(
        len(inlist) / (termwidth / ((maxlen + 4))),
    )
    columns = listsplit(tmplist, column_number)
    listlist = []
    for elem in columns:
        listlist.append(elem)
    maxlen2 = len(max(listlist, key=len))
    for sublist in listlist:
        while len(sublist) < maxlen2:
            sublist.append("")
    if space:
        print()
    for row in zip(*listlist):
        tstr = ""
        for i in row:
            tstr = tstr + "{0:{1}}".format(i, maxlen)  # + "  "
        print(tstr)
    print()


def dict_formatter(outdict):
    """
    Formats dicts for display in the shell.
    """
    for key in outdict.keys():
        print("{0}   {1} {2}{3}{0}: {4}".format(
            color.END, ENUM, color.BOLD, key, outdict[key],
        ))
    print()


def ldis():
    """
    print a legal warning on the terminal
    """
    if SHOW_WARNING:
        print(
            """     {0}_________________________________________________{1}
     {2}  The developers assume no liability and aren't  {1}
     {2}  amenable for any misuse or damage caused. Do   {1}
     {2}  not deploy illicitly or maliciously.           {1}
     {0}{3}{1}
            """.format(
                color.RD, color.END, color.RBC, lines.OL * 49,
            )
        )


"""
the following methods nicely output lists for payload selection
and result output
"""


def listprint2(plist, nullbytes, wrappers):
    pstr = ""
    for i in range(0, len(plist)):
        pstr = pstr + "{0}{1:{5}}{2}{6}{3}  {4}\n".format(
            "", i, "", "", plist[i],
            len(str(len(payloadlist))), lines.VL,
        )
    pstr = pstr + "{0}{1}{4}{2}  {3}\n".format(
        "", "  A", "", "ALL", lines.VL,
    )
    if nullbytes or wrappers:
        pstr = pstr + "{0}{1}{4}{2}  {3}\n".format(
            "", "  N", "", "NONE", lines.VL,
        )
    return pstr


def listprint(plist, nullbytes, wrappers):
    tmplist = []
    for i in range(0, len(plist)):
        tmpstr = "{0}{1:{5}}{2}{6}{3}  {4}".format(
            color.RB, i, color.END + color.RD, color.END,
            plist[i], len(str(len(payloadlist))),
            lines.VL,
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
    print("{0}{1}{4}{2}  {3}".format(
        color.RB,
        space + "A" + color.END + color.RD,
        color.END, "ALL", lines.VL,
    ))
    if nb or wrappers:
        print("{0}{1}{4}{2}  {3}".format(
            color.RB,
            space + "N" + color.END + color.RD,
            color.END, "NONE", lines.VL,
        ))
    print()


def table_print(old_tuple, not_implemented=False):
    new_tuple = []
    for elem in old_tuple:
        if not_implemented:
            new_tuple.append("{}{}{}".format(
                color.END + color.CURSIVE, elem, color.END + color.RD,
            ))
        else:
            new_tuple.append("{}{}{}".format(color.END, elem, color.RD))
    return tuple(new_tuple)


def table_entry_print(entry):
    formatted = []
    for payload in entry:
        formatted.append("{}{}{}".format(color.END, payload, color.RD))
    return ",\n".join(elem for elem in formatted)


def print_techniques_gui():
    tstr = ""
    items = rce.keys()
    for i in items:
        tstr = tstr + "{0}{1:{5}}{2}{6}{3}  {4}\n".format(
            "", i, "", "", rce[i],
            max(3, len(str(len(items)))),
            lines.VL,
        )
    tstr = tstr + "{0}{1}{4}{2}  {3}\n".format(
        "", "  A", "", "ALL", lines.VL,
    )
    return tstr


def print_techniques():
    tmplist = []
    items = rce.keys()
    for i in items:
        tmpstr = "{0}{1:{5}}{2}{6}{3}  {4}".format(
            color.RB, i, color.END + color.RD, color.END,
            rce[i], max(3, len(str(len(items)))),
            lines.VL,
        )
        tmplist.append(tmpstr)
    maxlen = len(max(tmplist, key=len))
    termwidth = shutil.get_terminal_size()[0]
    column_number = math.floor(len(items) / (termwidth / ((maxlen + 4))))
    columns = listsplit(tmplist, column_number)
    listdisplay(columns, maxlen, False, False)


def print_vectors_gui():
    vstr = ""
    items = vector_dict.keys()
    for i in items:
        vstr = vstr + "{0}{1:{5}}{2}{6}{3}  {4}\n".format(
            "", i, "", "", vector_dict[i],
            max(3, len(str(len(items)))),
            lines.VL,
        )
    vstr = vstr + "{0}{1}{4}{2}  {3}\n".format(
        "", "  A", "", "ALL", lines.VL,
    )
    return vstr


def print_vectors():
    tmplist = []
    items = vector_dict.keys()
    for i in items:
        tmpstr = "{0}{1:{5}}{2}{6}{3}  {4}".format(
            color.RB, i, color.END + color.RD, color.END,
            vector_dict[i], max(3, len(str(len(items)))),
            lines.VL,
        )
        tmplist.append(tmpstr)
    maxlen = len(max(tmplist, key=len))
    termwidth = shutil.get_terminal_size()[0]
    column_number = math.floor(len(items) / (termwidth / ((maxlen + 4))))
    columns = listsplit(tmplist, column_number)
    listdisplay(columns, maxlen, False, False)
