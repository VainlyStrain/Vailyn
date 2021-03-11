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


import sys
import argparse
import terminaltables

from core.colors import color, lines, FAIL, TRI

from core.config import ASCII_ONLY

from core.methods.print import table_print


class ArgumentParser(argparse.ArgumentParser):
    """
    Vailyn's argument parser
    """
    def error(self, message):
        self.print_help()
        self.exit(
            2,
            "\n" + color.R + f"[{FAIL}]" + color.END + color.BOLD
            + " Invalid/missing params" + color.END + "\n"
            + color.RD + "[HINT]" + color.END + " %s\n" % (message)
        )

    def print_help(self):
        DATA = [table_print(("TP", "P1", "P2"))]
        DATA.append(table_print(("leak", "File Dict", "Directory Dict")))
        DATA.append(table_print(("inject", "IP Addr", "Listening Port")))
        DATA.append(table_print(
            ("implant", "Source File", "Server Destination"),
            not_implemented=True,
        ))
        if ASCII_ONLY:
            table = terminaltables.AsciiTable(DATA, "[ {}Values{} ]".format(
                color.END,
                color.RD),
            ).table
        else:
            table = terminaltables.SingleTable(DATA, "[ {}Values{} ]".format(
                color.END,
                color.RD),
            ).table
        self.print_usage(sys.stderr)
        print("""
{5}mandatory{6}{1}
  -v VIC, --victim VIC  {0}Target to attack, part 1 [pre-payload]{1}
  -a INT, --attack INT  {0}Attack type (int, 1-5, or A){1}

  {2}  A{1}{3}{7}{1}  Spider (all)     {2}  2{1}{3}{7}{1}  Path             {2}  5{1}{3}{7}{1}  POST Data, json
  {2}  P{1}{3}{7}{1}  Spider (partial) {2}  3{1}{3}{7}{1}  Cookie
  {2}  1{1}{3}{7}{1}  Query Parameter  {2}  4{1}{3}{7}{1}  POST Data, plain{1}

  -p2 TP P1 P2, --phase2 TP P1 P2
                        {0}Attack in Phase 2, and needed parameters{1}

{3}{4}{1}

{5}additional{6}{1}
  -p PAM, --param PAM   {0}query parameter or POST data for --attack 1, 4, 5{1}
  -i F, --check F       {0}File to check for in Phase 1 (df: etc/passwd){1}
  -Pi VIC2, --vic2 VIC2 {0}Attack Target, part 2 [post-payload]{1}
  -c C, --cookie C      {0}Cookie to append (in header format){1}
  -l, --loot            {0}Download found files into the loot folder{1}
  -d I J K, --depths I J K
                        {0}depths (I: phase 1, J: phase 2, K: permutation level){1}
  -h, --help            {0}show this help menu and exit{1}
  -s T, --timeout T     {0}Request Timeout; stable switch for Arjun{1}
  -t, --tor             {0}Pipe attacks through the Tor anonymity network{1}
  -L, --lfi             {0}Additionally use PHP wrappers to leak files{1}
  -n, --nosploit        {0}skip Phase 2 (does not need -p2 TP P1 P2){1}
  -P, --precise         {0}Use exact depth in Phase 1 (not a range){1}
  -A, --app             {0}Start Vailyn's Qt5 interface{1}

{5}develop{6}{1}
  --debug               {0}Display every path tried, even 404s.{1}
  --version             {0}Print program version and exit.{1}
  --notmain             {0}Avoid notify2 crash in subprocess call.{1}""".format(
            color.RC, color.END, color.RB, color.RD, table,
            color.RBB, TRI, lines.VL,
        ))


class VainFormatter(argparse.RawDescriptionHelpFormatter):
    """
    Formatter for the argument parser
    """
    def add_usage(self, usage, actions, groups, prefix=None):
        if prefix is None:
            prefix = color.RC + "Vsynta " + color.END
            return super(VainFormatter, self).add_usage(
                "{}Vailyn{} -v VIC -a INT -p2 TP P1 P2 \n".format(
                    color.RB, color.END,
                )
                + "        [-p PAM] [-i F] [-Pi VIC2]\n"
                + "      [-c C] [-n] [-d I J K]\n"
                + "       [-s T] [-t] [-L]\n"
                + "  [-l] [-P] [-A] ",
                actions,
                groups,
                prefix
            )


def parser():
    """
    constructs and returns an argument parser
    """
    p = ArgumentParser(formatter_class=VainFormatter, add_help=False)
    p.add_argument("-v", "--victim",
                   help="Target to attack, part 1 [pre injection point]",
                   metavar="VIC")
    p.add_argument("-a", "--attack",
                   help="Attack type (int, 1-5 or A)[see the Markdown docs]",
                   metavar="INT")
    p.add_argument("-s", "--timeout",
                   help="Request Timeout; stable switch for Arjun",
                   metavar="T",
                   type=int)
    p.add_argument("-d", "--depths",
                   help="depths (I: phase 1, J: phase 2, K: permutation level)",
                   metavar="I J K",
                   type=int,
                   nargs=3)
    p.add_argument("-h", "--help",
                   help="0 » display this help message and exit",
                   action="help",
                   default=argparse.SUPPRESS)
    p.add_argument("-p", "--param",
                   help="query parameter & post data to use",
                   metavar="P")
    p.add_argument("-p2", "--phase2",
                   help="Phase 2 and needed parameters",
                   nargs=3,
                   metavar=("TP", "P1", "P2"))
    p.add_argument("-l", "--loot",
                   help="Download found files into the loot folder",
                   action="store_true")
    p.add_argument("-Pi", "--vic2",
                   help="Attack Target, part 2 (post injection point)",
                   metavar=("V"))
    p.add_argument("-i", "--check",
                   help="File to check for in Phase 1 (df: etc/passwd)",
                   metavar=("F"))
    p.add_argument("-c", "--cookie",
                   help="Cookie to append (in header format)",
                   metavar=("C"))
    p.add_argument("-t", "--tor",
                   help="Pipe attacks through the Tor anonymity network",
                   action="store_true",)
    p.add_argument("--debug",
                   help="display every path tried, even 404s",
                   action="store_true",)
    p.add_argument("-n", "--nosploit",
                   help="skip Phase 2 (does not need -p2 TP P1 P2)",
                   action="store_true",)
    p.add_argument("-P", "--precise",
                   help="Use absolute Phase 1 Depth (not range)",
                   action="store_true",)
    p.add_argument("-A", "--app",
                   help="Start Vailyn's Qt5 interface",
                   action="store_true",)
    p.add_argument("--version",
                   help="Print program version and exit.",
                   action="store_true",)
    p.add_argument("-L", "--lfi",
                   help="Use LFI wrappers to leak files",
                   action="store_true",)
    p.add_argument("--notmain",
                   help="Vailyn is executed as subprocess.",
                   action="store_true",)

    return p
