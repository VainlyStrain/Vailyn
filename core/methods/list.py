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

def listperm(sdirs, depth):
    #print("sdirs: {}".format(sdirs))
    for idir in sdirs:
        yield idir
    iter=1
    ndirs=list.copy(sdirs)
    #remove empty string causing duplicates
    del ndirs[0]
    mdirs=[]
    while (iter<=(depth)):
        for mdirs in permutations(ndirs,(iter+1)):
            #print("mdirs: {}".format(mdirs))
            diri = ""
            for elem in mdirs:
                diri += str(elem)
            yield diri
                #sdirs.append(diri)
        iter+=1

def gensplit(g, n):
    i = iter(g)
    piece = list(islice(i, n))
    while piece:
        yield piece
        piece = list(islice(i, n))
        