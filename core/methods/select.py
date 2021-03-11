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


from core.colors import color, lines
from core.methods.print import listprint, print_techniques, print_vectors
from core.variables import rce, vector_count
from core.variables import payloadlist as totalpayloadlist


def select(payloadlist, nullbytes=False, wrappers=False, nosploit=False):
    """
    select specific payloads or nullbytes for phase 2
    @params:
        payloadlist - payloads or nullbytes found in phase 1
    """
    # filter duplicates
    payloadlist = list(set(payloadlist))
    if nullbytes:
        print("\n{0}[+]{1}{2} {3:{4}}{1}{0}{5}{1}".format(
            color.RD,
            color.END,
            color.RB,
            len(payloadlist),
            len(str(len(totalpayloadlist))),
            lines.VL,
        ) + " Operative nullbytes:")
    elif wrappers:
        print("\n{0}[+]{1}{2} {3:{4}}{1}{0}{5}{1}".format(
            color.RD,
            color.END,
            color.RB,
            len(payloadlist),
            len(str(len(totalpayloadlist))),
            lines.VL,
        ) + " Operative PHP wrappers:")
    else:
        print("\n{0}[+]{1}{2} {3:{4}}{1}{0}{5}{1}".format(
            color.RD,
            color.END,
            color.RB,
            len(payloadlist),
            len(str(len(totalpayloadlist))),
            lines.VL,
        ) + " Operative payloads:")

    listprint(payloadlist, nullbytes, wrappers)
    invalid = True
    while invalid:
        if not nosploit:
            payloads = input(
                "{0}[?]{1}{3}{4}{1}{0}{8}{1}{5}{0} {7}{1} {2}{6}{1} :> ".format(
                    color.RD, color.END, color.CURSIVE, color.RB,
                    " Payloads", " Select indices\n", "comma-separated",
                    lines.SW, lines.VL,
                )
            )
            try:
                if payloads.strip().lower() == "a":
                    return payloadlist
                elif (
                    (nullbytes or wrappers)
                    and payloads.strip().lower() == "n"
                ):
                    return []
                selected = [
                    payloadlist[int(i.strip())] for i in payloads.split(",")
                ]
                invalid = False
            except Exception:
                pass
        else:
            selected = []
            invalid = False
    return selected


def select_techniques():
    """
    select techniques to use in RCE module
    @return:
        selected techniques, as a list
    """
    techniques = []
    invalid = True
    print_techniques()
    while invalid:
        selected = input(
            "{0}[?]{1}{3}{4}{1}{0}{8}{1}{5}{0} {7}{1} {2}{6}{1} :> ".format(
                color.RD, color.END, color.CURSIVE, color.RB,
                " Techniques", " Select indices\n", "comma-separated",
                lines.SW, lines.VL,
            )
        )
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


def select_vectors():
    """
    select vectors to use in custom crawler mode
    @return:
        selected vectors, as a list
    """
    vectors = []
    invalid = True
    print_vectors()
    while invalid:
        selected = input(
            "{0}[?]{1}{3}{4}{1}{0}{8}{1}{5}{0} {7}{1} {2}{6}{1} :> ".format(
                color.RD, color.END, color.CURSIVE, color.RB,
                " Vectors", " Select indices\n", "comma-separated",
                lines.SW, lines.VL,
            )
        )
        try:
            error = False
            if selected.strip().lower() == "a":
                return list(range(1, vector_count + 1))
            for i in selected.split(","):
                vector = int(i.strip())
                if vector not in range(1, vector_count + 1):
                    error = True
                elif vector not in vectors:
                    vectors.append(vector)
            if vectors and not error:
                invalid = False
            else:
                vectors = []
        except Exception:
            pass

    return vectors
