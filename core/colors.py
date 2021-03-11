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


from core.config import ASCII_ONLY


class color:
    BOLD = "\033[1m"
    UNDERLINE = "\033[4m"
    CURSIVE = "\033[3m"
    END = "\033[0m"
    G = "\033[0m\033[48;2;225;214;225m\033[38;2;58;49;58m\033[1m"
    C = "\033[0m\033[1m"
    RB = "\033[48;2;42;35;42m"
    RC = "\033[0m\033[38;2;58;49;58m\033[3m"
    RD = "\033[0m\033[38;2;58;49;58m"
    R = "\033[1m\033[38;2;58;49;58m"
    RBC = "\033[0m\033[48;2;42;35;42m\033[1m\033[3m"
    RBB = "\033[0m\033[48;2;42;35;42m\033[1m"


FAIL = "-" if ASCII_ONLY else "✗"
SUCCESS = "+" if ASCII_ONLY else "✓"
TRI = ":" if ASCII_ONLY else u"\033[0m\033[38;2;42;35;42m\uE0B0"


class lines:
    SW = "'--" if ASCII_ONLY else "└──"
    SWL = "'---" if ASCII_ONLY else "└──╼"
    NW = ".-" if ASCII_ONLY else "┌─"
    OL = " " if ASCII_ONLY else "‾"
    VL = "|" if ASCII_ONLY else "│"
