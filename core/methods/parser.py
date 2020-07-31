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

import sys, argparse
from core.colors import color

class ArgumentParser(argparse.ArgumentParser):
    def error(self, message):
        self.print_usage(sys.stderr)
        self.exit(2, "\n"+color.R+'[-]'+color.END+color.BOLD+' Invalid/missing params'+color.END+'\n'+color.RD+'[HINT]'+color.END+' %s\n' % (message))
    def print_help(self):
        self.print_usage(sys.stderr)
        print('''
mandatory:
  -v VIC, --victim VIC  {0}Target to attack, part 1 [pre injection point]{1}
  -a ACK, --attack ACK  {0}Attack type (int)[1: query, 2: path, 3:cookie]{1}
  -l FIL PATH, --lists FIL PATH      
                        {0}Dictionaries to use (see templates for syntax){1}
additional:
  -p PAM, --param PAM   {0}query parameter to use for --attack 1{1}
  -s DAT, --post DAT    {0}POST Data (set injection point with INJECT){1}
  -d I J, --depths I J  {0}depths of checking (I: phase 1, J: phase 2){1}
  -n, --loot            {0}Download found files into the loot folder{1}
  -c FIL, --cookie FIL  {0}File containing authentication cookie (if needed){1}
  -h, --help            {0}show this help menu and exit{1}
  -i FIL, --check FIL   {0}File to check for in Phase 1 (df: /etc/passwd){1}
  -q VIC2, --vic2 VIC2  {0}Attack Target, part 2 (post injection point){1}
  -t, --tor             {0}Pipe attacks through the Tor anonymity network{1}
  --app                 {0}Start Vailyn's Qt5 interface{1}'''.format(color.RC, color.END))

class VainFormatter(argparse.RawDescriptionHelpFormatter):
    def add_usage(self, usage, actions, groups, prefix=None):
        if prefix is None:
            prefix = color.RC + 'Vsynta ' + color.END
            #return super(VainFormatter, self).add_usage("{}Vailyn{} [-v VIC] [-a ACK] [-p PARAM] [-s]\n          [-l FIL PATH] [-d INT] [--loot]\n        [-f] [-h] [--vic2 VIC2]".format(color.RB,color.END), actions, groups, prefix)
            return super(VainFormatter, self).add_usage("{}Vailyn{} -v VIC -a ACK -l FIL PATH \n        [-p PAM] [-s DAT] [-d I J] \n      [-c FIL] [-i FIL] [-n]\n        [-t] [--app] \n    [-q VIC2]".format(color.RB,color.END), actions, groups, prefix)

def build_parser():
    p = ArgumentParser(formatter_class=VainFormatter,add_help=False)
    p.add_argument('-v', '--victim',
                   help="Target to attack, part 1 [pre injection point]",
                   metavar="VIC")
    p.add_argument('-a', '--attack',
                   help="Attack type (int)[1: query, 2: path, 3:cookie]",
                   metavar="ACK",
                   type=int)
    p.add_argument('-s', '--post',
                   help="POST Data (set injection point with INJECT)",
                   metavar="DAT",)
    p.add_argument('-d', '--depths',
                   help="depths of checking (I: phase 1, J: phase 2)",
                   metavar="I J",
                   type=int,
                   nargs=2)
    p.add_argument('-h', '--help',
                   help="0 » display this help message and exit",
                   action="help",
                   default=argparse.SUPPRESS)
    p.add_argument('-p', '--param',
                   help="query parameter to use for --attack 1",
                   metavar="PAM")
    p.add_argument('-l', '--lists',
                   help="Dictionaries to use (see templates for syntax)",
                   nargs=2,
                   metavar=("FIL","PATH"))
    p.add_argument('-n', '--loot',
                   help="Download found files into the loot folder",
                   action="store_true")
    p.add_argument('-q', '--vic2',
                   help="Attack Target, part 2 (post injection point)",
                   metavar=("VIC2"))
    p.add_argument('-i', '--check',
                   help="File to check for in Phase 1 (df: /etc/passwd)",
                   metavar=("FIL"))
    p.add_argument('-c', '--cookie',
                   help="File containing authentication cookie (if needed)",
                   metavar=("FIL"))
    p.add_argument('-t', '--tor',
                   help="Pipe attacks through the Tor anonymity network",
                   action="store_true",)
    p.add_argument('--debug',
                   help="display every path tried, even 404s",
                   action="store_true",)
    p.add_argument('--app',
                   help="Start Vailyn's Qt5 interface",
                   action="store_true",)
               
    return p 
