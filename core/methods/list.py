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


from itertools import permutations, islice, combinations

"""equally split list for threads"""
def listsplit(l, n):
    if n == 0:
        n += 1
    for i in range(0, len(l), n):
        yield l[i:i + n]  

"""
create directory dictionary permutations
generator to be more memory-friendly
"""
def listperm(sdirs, depth):
    for idir in filegen(sdirs, dirs=True):
        yield idir
        #print(idir)
    iter=1
    """
    TODO avoid list copy, improve memory footprint further
    """

    #remove empty string causing duplicates
    mdirs=[]
    while (iter<=(depth)):
        ndirs = filegen(sdirs)
        for mdirs in permutations(ndirs,(iter+1)):
            diri = ""
            for elem in mdirs:
                diri += str(elem)
            yield diri
            #print(diri)
        iter+=1

"""
equally split generator elements for threads
"""
def gensplit(g, n):
    i = iter(g)
    piece = list(islice(i, n))
    while piece:
        yield piece
        piece = list(islice(i, n))

"""read dictionary file into generator"""
def filegen(path, dirs=False):
    if dirs:
        yield ""
    with open(path, "r") as dfile:
        for line in dfile:
            if dirs and not line.strip().endswith("/"):
                line = line.strip() + "/"
            yield line.strip()
