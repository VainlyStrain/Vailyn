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
    def print_help(self):
        self.print_usage(sys.stderr)
        print('''

  -v VIC, --victim VIC  {0}Target to attack, part 1 (pre injection point){1}
  -a ACK, --attack ACK  {0}Type of attack [int](1: query, 2: path){1}
  -l FIL PATH, --lists FIL PATH      
                        {0}Dictionaries to use (see templates for syntax){1}
  -p PAM, --param PAM   {0}query parameter to use for --attack 1{1}
  -s, --summary         {0}Print a summary of found files and payloads{1}
  -d INT, --depth INT   {0}max. nr of ../ and dir permutation level [int]{1}
  -f, --verbosity       {0}display every path tried, even 404s{1}
  -n, --loot            {0}Download found files into the loot folder{1}
  -c FIL, --check FIL   {0}File to check for in Phase 1 (df: /etc/passwd){1}
  -q VIC2, --vic2 VIC2  {0}Attack Target, part 2 (post injection point){1}'''.format(color.RC, color.END))

class VainFormatter(argparse.RawDescriptionHelpFormatter):
    def add_usage(self, usage, actions, groups, prefix=None):
        if prefix is None:
            prefix = color.RC + 'Vsynta ' + color.END
            #return super(VainFormatter, self).add_usage("{}Vailyn{} [-v VIC] [-a ACK] [-p PARAM] [-s]\n          [-l FIL PATH] [-d INT] [--loot]\n        [-f] [-h] [--vic2 VIC2]".format(color.RB,color.END), actions, groups, prefix)
            return super(VainFormatter, self).add_usage("{}Vailyn{} -v VIC -a ACK -l FIL PATH [-s]\n        [-p PAM] [-q VIC2] [-d INT] \n      [-n] [-c FIL] [-f]".format(color.RB,color.END), actions, groups, prefix)

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
    p.add_argument('-q', '--vic2',
                   help="A › Attack target part 2",
                   metavar=("VIC2"))
    p.add_argument('-c', '--check',
                   help="A › Attack target part 2",
                   metavar=("FILE"))
               
    return p 
