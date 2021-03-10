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


from itertools import permutations, islice


def listsplit(inp_list, n):
    """
    equally split list for threads
    """
    if n == 0:
        n += 1
    for i in range(0, len(inp_list), n):
        yield inp_list[i:i + n]


def listperm(sdirs, depth):
    """
    create directory dictionary permutations
    generator to be more memory-friendly
    """
    for idir in filegen(sdirs, dirs=True):
        yield idir

    iter = 1

    # remove empty string causing duplicates
    mdirs = []
    while (iter <= depth):
        ndirs = filegen(sdirs)
        for mdirs in permutations(ndirs, (iter + 1)):
            diri = ""
            for elem in mdirs:
                diri += str(elem)
            yield diri
        iter += 1


def gensplit(g, n):
    """
    equally split generator elements for threads
    """
    i = iter(g)
    piece = list(islice(i, n))
    while piece:
        yield piece
        piece = list(islice(i, n))


def filegen(path, dirs=False):
    """
    read dictionary file into generator
    """
    if dirs:
        yield ""
    with open(path, "r") as dfile:
        for line in dfile:
            if dirs and not line.strip().endswith("/"):
                line = line.strip() + "/"
            yield line.strip()
