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
    for idir in sdirs:
        yield idir
    iter=1
    """
    TODO avoid list copy, improve memory footprint further
    """
    ndirs=list.copy(sdirs)
    #remove empty string causing duplicates
    del ndirs[0]
    mdirs=[]
    while (iter<=(depth)):
        for mdirs in permutations(ndirs,(iter+1)):
            diri = ""
            for elem in mdirs:
                diri += str(elem)
            yield diri
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
        