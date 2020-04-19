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

import treelib, string, random
from core.colors import color

def randomword(length):
   letters = string.ascii_lowercase
   return ''.join(random.choice(letters) for i in range(length))

def replaceColors(ntag):
    return ntag.replace(color.RD, "").replace(color.END, "")
    

def tree_append(tree, path, parentnode):
    plist = path.split("/")
    id = plist[0]
    if not tree.contains(id):
        tree.create_node(color.END+plist[0]+color.RD, id, parent=parentnode)
    else:
        if tree.parent(id).identifier != parentnode:
            new = True
            for i in tree.children(parentnode):
                if replaceColors(i.tag) == id:
                    new = False
            if new:
                id = id + randomword(128)
                tree.create_node(color.END+plist[0]+color.RD, id, parent=parentnode)
    if len(plist) > 1:
        tree_append(tree, "/".join(plist[1::]), id)
        
def create_tree(tree, filepaths):
    for i in filepaths:
        if i != "":
            tree_append(tree, i, "root")
