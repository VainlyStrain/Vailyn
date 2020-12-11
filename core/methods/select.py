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
from core.methods.print import listprint, printTechniques
from core.variables import rce
from core.variables import payloadlist as totalpayloadlist


def select(payloadlist, nullbytes=False, nosploit=False):
    """
    select specific payloads or nullbytes for phase 2
    @params:
        payloadlist - payloads or nullbytes found in phase 1
    """
    # filter duplicates
    payloadlist = list(set(payloadlist))
    if nullbytes:
        print("\n{0}[+]{1}{2} {3:{4}}{1}{0}|{1} Operative nullbytes:".format(
                color.RD, color.END, color.O, len(payloadlist), len(str(len(totalpayloadlist)))
            ))
    else:
        print("\n{0}[+]{1}{2} {3:{4}}{1}{0}|{1} Operative payloads:".format(
                color.RD, color.END, color.O, len(payloadlist), len(str(len(totalpayloadlist)))
            ))

    listprint(payloadlist, nullbytes)
    invalid = True
    while invalid:
        if not nosploit:
            payloads = input("{0}[?]{1}{3} Payloads{1}{0}|{1} Select indices\n{0} └──{1} {2}comma-separated{1} :> ".format(
                                color.RD, color.END, color.CURSIVE, color.O
                            ))
            try:
                if payloads.strip().lower() == "a":
                    return payloadlist
                elif nullbytes and payloads.strip().lower() == "n":
                    return []
                selected = [payloadlist[int(i.strip())] for i in payloads.split(",")]
                invalid = False
            except Exception:
                pass
        else:
            selected = []
            invalid = False
    return selected


def selectTechniques():
    """
    select techniques to use in RCE module
    @return:
        selected techniques, as a list
    """
    techniques = []
    invalid = True
    printTechniques()
    while invalid:
        selected = input("{0}[?]{1}{3} Techniques{1}{0}|{1} Select indices\n{0} └──{1} {2}comma-separated{1} :> ".format(
                            color.RD, color.END, color.CURSIVE, color.O
                        ))
        try:
            error = False
            if selected.strip().lower() == "a":
                return list(range(1, len(rce.items()) + 1))
            for i in selected.split(","):
                technique = int(i.strip())
                if technique not in range(1, len(rce.items()) + 1):
                    error = True
                elif technique not in techniques:
                    techniques.append(technique)
            if techniques and not error:
                invalid = False
            else:
                techniques = []
        except Exception:
            pass

    return techniques