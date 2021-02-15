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


class ShellPopException(Exception):
    """
    This exception will be raised if a reverse shell
    has been received. This is done to terminate the
    program, because all techniques coming after the
    successful one would be counted as successful.
    """
    pass
