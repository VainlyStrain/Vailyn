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
       

┌─[pathtrav]─[~]
└──╼ VainlyStrain
"""

import sys, argparse
from core.colors import color

class ArgumentParser(argparse.ArgumentParser):
    def error(self, message):
        self.print_usage(sys.stderr)
        self.exit(2, "\n"+color.R+'[-]'+color.END+color.BOLD+' Invalid/missing params'+color.END+'\n'+color.RD+'[HINT]'+color.END+' %s\n' % (message))

class VainFormatter(argparse.RawDescriptionHelpFormatter):
    def add_usage(self, usage, actions, groups, prefix=None):
        if prefix is None:
            prefix = color.RC + 'Vsynta.: ' + color.END
            #return super(VainFormatter, self).add_usage("{}pathleak{} [-v VIC] [-a ACK] [-p PARAM] [-s]\n          [-l FIL PATH] [-d INT] [--loot]\n        [-f] [-h] [--vic2 VIC2]".format(color.RB,color.END), actions, groups, prefix)
            return super(VainFormatter, self).add_usage("{}pathleak{} -v VIC -a ACK -l FIL PATH\n          [-p PAM] [-s] [-d INT] [-f]\n        [-n] [-c VIC2]".format(color.RB,color.END), actions, groups, prefix)

def build_parser():
    p = ArgumentParser(formatter_class=VainFormatter,add_help=False)
    p.add_argument('-v', '--victim',
                   help="set attack target address [scheme:// needed]",
                   metavar="VIC")
    p.add_argument('-a', '--attack',
                   help="attack [1]:query [2]:inpath",
                   metavar="ACK",
                   type=int)
    p.add_argument('-f', '--verbosity',
                   help="Show 404s?",
                   action="store_true",)
    p.add_argument('-s', '--summary',
                   help="No Output until scan finished?",
                   action="store_true",)
    p.add_argument('-d', '--depth',
                   help="1 › max. nr of ../ and dir permutation level",
                   metavar="INT",
                   type=int)
    p.add_argument('-h', '--help',
                   help="0 » display this help message and exit",
                   action="help",
                   default=argparse.SUPPRESS)
    p.add_argument('-p', '--param',
                   help="A › Query parameter for file",
                   metavar="PARAM")
    p.add_argument('-l', '--lists',
                   help="1 » Dictionaries",
                   nargs=2,
                   metavar=("FIL","PATH"))
    p.add_argument('-n', '--loot',
                   help="1 › Download found files into loot",
                   action="store_true")
    p.add_argument('-c', '--vic2',
                   help="A › Attack target part 2",
                   metavar=("VIC2"))
               
    return p 
