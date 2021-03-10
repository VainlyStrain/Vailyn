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

import string
import random
from core.colors import color


def random_word(length):
    """
    generates a random string, used for unique tree ids when
    duplicate file names

    @params:
        length - length of the result string.
    """
    letters = string.ascii_lowercase
    return "".join(
        random.choice(letters) for i in range(length)
    )


def replace_colors(ntag):
    """
    removes Vailyn's colors from string
    @params:
        ntag - string to be handled.
    """
    tag = ntag.replace(color.RD, "")
    tag = tag.replace(color.END, "")
    tag = tag.replace(color.RB, "")
    tag = tag.replace(color.CURSIVE, "")
    tag = tag.replace(color.BOLD, "")

    return tag


def tree_append(tree, path, parentnode):
    """
    append file to found files tree
    @params:
        tree       - tree to operate on.
        path       - path of the file.
        parentnode - node to be operated on.
    """
    plist = path.split("/")
    id = plist[0]
    if not tree.contains(id):
        if len(plist) > 1:
            tree.create_node(
                color.END + color.CURSIVE + color.END
                + plist[0] + color.RD,
                id,
                parent=parentnode,
            )
        else:
            tree.create_node(
                color.END + color.CURSIVE + plist[0]
                + color.END + color.RD,
                id,
                parent=parentnode,
            )
    else:
        if tree.parent(id).identifier != parentnode:
            new = True
            for i in tree.children(parentnode):
                if replace_colors(i.tag) == id:
                    new = False
            if new:
                id = id + random_word(128)
                if len(plist) > 1:
                    tree.create_node(
                        color.END + plist[0] + color.RD,
                        id,
                        parent=parentnode,
                    )
                else:
                    tree.create_node(
                        color.END + color.CURSIVE
                        + plist[0] + color.END + color.RD,
                        id,
                        parent=parentnode,
                    )
    if len(plist) > 1:
        tree_append(tree, "/".join(plist[1::]), id)


def create_tree(tree, filepaths):
    """
    populate the found files tree
    @params:
        tree      - the empty tree structure.
        filepaths - paths of all found files.
    """
    for i in filepaths:
        contained = False
        # prevent dups if parent folder found
        for j in filepaths:
            if i != j and i != "" and i in j:
                contained = True
        if i != "" and not contained:
            tree_append(tree, i, "root")
