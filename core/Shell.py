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


from core.colors import (
    color, lines, FAIL, FAIL2, SUCCESS, TRI_1, TRI_2,
)
from core.config import ASCII_ONLY
from core.variables import version

from core.methods.print import (
    intro, help_formatter, dict_formatter, table_print,
)

from cmd import Cmd

from terminaltables import AsciiTable, SingleTable

import sys


def update_prompt(target="n/a", vector="n/a"):
    prompt = ""
    if ASCII_ONLY:
        prompt = "Vailyn v{}".format(version)
        if target != "n/a" or vector != "n/a":
            prompt += "({}:{})".format(target, vector)
        prompt += " > "
    else:
        prompt += "{} # {} ".format(color.RBC, color.INP)
        prompt += "Vailyn{}".format(version)
        prompt += " {0}{2}[{1}-▸{3}]{0}".format(
            color.END, target, color.RC, vector,
        )
        prompt += "\n{}┗▸ {}".format(color.RF, color.INP)

    return prompt


class VailynShell(Cmd):
    intro = ""
    prompt = update_prompt()
    attack_config = {
        "VICTIM": ["", "Target Link to attack."],
        "ATTACK": ["", "Attack Vector to use. (see list VECTORS)"],
        "PHASE2": ["", "Phase 2 to use, with arguments. (see list PHASE2)"],
        "INPOINT": ["", "Injection Point. (parameter)"],
        "CHECK": ["", "File to check for in Phase 1."],
        "LOOT": ["0", "Download leaked files. (0/1)"],
        "DEPTHS": ["", "Lookup Depths. (P1, P2, PL)"],
        "PRECISE": ["0", "Use exact P1 Depth (0/1)"],
        "COOKIE": ["", "Authentication Cookie String."],
        "FILTER": ["0", "Use php://filter in Phase 1. (0/1)"],
        "TIMEOUT": ["", "Request Timeout. (also Arjun stable)"],
        "VICTIM2": ["", "Target Link, part 2."],
    }

    list_sets = {
        "CONFIG": "Vailyn Core configuration options.",
        "OPTIONS": "Vailyn Attack configuration options.",
        "PHASE2": "All supported options for the exploitation phase.",
        "VECTORS": "All supported vectors for Options.ATTACK.",
    }

    vector_list = {
        "ALL": "Automatically scan all pages using all vectors.",
        "PARTIAL": "Automatically scan all pages using a selection of vectors.",
        "QUERY": "Scan a query GET parameter of a single page.",
        "PATH": "Scan a single page using the URL path itself.",
        "COOKIE": "Scan a delivered cookie from a single page.",
        "POST_PLAIN": "Scan POST plain data of a single page.",
        "POST_JSON": "Scan POST JSON data of a single page.",
    }

    sploit_list = {
        "LEAK <File Dict> <Directory Dict>": "Leak files from server using dictionaries.",
        "INJECT <IP Addr> <Listening Port>": "Perform LFI RCE to spawn a reverse shell.",
        "IMPLANT <Source File> <Server Destination>": "Use upload path traversal to replace files.",
        "NOSPLOIT": "Skip Phase 2.",
    }

    def info(self):
        print("foo")

    def error(self, msg, cmd):
        print("{0}[{3}]{2}{1}  {5}{2}{0}{4}{2} {6}".format(
            color.RD, color.RB, color.END,
            color.BOLD + FAIL2 + color.END + color.RD,
            lines.VL, cmd, msg,
        ))

    def cmdloop(self, intro=None):
        while True:
            try:
                super(VailynShell, self).cmdloop(intro=None)
                break
            except KeyboardInterrupt:
                print("^C")
                sys.exit(0)

    def do_help(self, arg):
        """
        override the default help function to point to our help menu
        """
        if arg:
            # XXX check arg syntax
            try:
                func = getattr(self, 'help_' + arg)
            except AttributeError:
                try:
                    doc = getattr(self, 'do_' + arg).__doc__
                    if doc:
                        self.stdout.write("%s\n" % str(doc))
                        return
                except AttributeError:
                    pass
                self.stdout.write("%s\n" % str(self.nohelp % (arg,)))
                return
            func()
        else:
            self.info()

    def help_help(self):
        title = "?, help"
        syntax_str = "help [CMD]"
        args = {"CMD": "The command to display a help message for."}
        description = """Shows information about a given command, or displays
the list of accepted commands."""
        examples = ["help", "help set"]
        help_formatter(
            title, description, args=args, syntax=syntax_str,
            examples=examples,
        )

    def do_q(self, inp):
        return True

    def help_q(self):
        help_formatter("q", "Quit Application.")

    def emptyline(self):
        pass

    def do_intro(self, inp):
        intro()
        intro(shell=True)

    def help_intro(self):
        help_formatter("intro", "Display Vailyn's asciiart.")

    def do_set(self, inp):
        listed = inp.split(" ")
        if len(listed) != 2:
            self.help_set()
        else:
            param = listed[0].strip().upper()
            value = listed[1].strip()
            if param not in self.attack_config.keys():
                self.error(
                    "Option {} not defined.".format(param),
                    "set()",
                )
                self.do_list("OPTIONS")
                return
            else:
                self.attack_config[param][0] = value
                print("{0}{1}{2}{3}{2}{4}{5}{2}{6}{2}".format(
                    color.END + color.RB, param, color.END, TRI_2,
                    color.G, value, TRI_1,
                ))
                victim = "n/a"
                vector = "n/a"
                if self.attack_config["VICTIM"][0]:
                    victim = self.attack_config["VICTIM"][0]
                if self.attack_config["ATTACK"][0]:
                    vector = self.attack_config["ATTACK"][0]
                self.prompt = update_prompt(target=victim, vector=vector)
        return

    def help_set(self):
        title = "set"
        description = """Set a value for a parameter needed for the attack.
Parameter names listed via {}list{} OPTIONS.""".format(color.BOLD, color.END,)
        args = {
            "OPT": "Name of the option to configure.",
            "VAL": "Value the option will take.",
        }
        syntax = "set OPT VAL"
        examples = [
            "set PHASE2 LEAK <path> <path>",
            "set LOOT 1",
            "set DEPTHS 8 8 1",
        ]
        further = [
            "{}list{} OPTIONS".format(color.BOLD, color.END,),
            "{}list{} VECTORS".format(color.BOLD, color.END,),
            "{}list{} PHASE2".format(color.BOLD, color.END,),
        ]
        help_formatter(
            title, description, syntax=syntax, args=args,
            examples=examples, further=further,
        )

    def do_list(self, inp):
        inp = inp.strip().upper()
        if inp == "OPTIONS":
            DATA = [table_print(
                ("Name", "Value", "Desc."),
            )]
            for (key, item) in self.attack_config.items():
                DATA.append(table_print(
                    (key, item[0], item[1]),
                ))
            if ASCII_ONLY:
                table = AsciiTable(DATA, "[ {0}{2}{1} ]".format(
                    color.END + color.BOLD,
                    color.END + color.RD,
                    "OPTIONS",
                ))
            else:
                table = SingleTable(DATA, "[ {0}{2}{1} ]".format(
                    color.END + color.BOLD,
                    color.END + color.RD,
                    "OPTIONS",
                ))
            print("\n" + color.RD + table.table + color.END + "\n")
        elif inp == "VECTORS":
            DATA = [table_print(
                ("Vector", "Desc."),
            )]
            for (key, item) in self.vector_list.items():
                DATA.append(table_print(
                    (key, item),
                ))
            if ASCII_ONLY:
                table = AsciiTable(DATA, "[ {0}{2}{1} ]".format(
                    color.END + color.BOLD,
                    color.END + color.RD,
                    "VECTORS",
                ))
            else:
                table = SingleTable(DATA, "[ {0}{2}{1} ]".format(
                    color.END + color.BOLD,
                    color.END + color.RD,
                    "VECTORS",
                ))
            print("\n" + color.RD + table.table + color.END + "\n")
        elif inp == "PHASE2":
            DATA = [table_print(
                ("Syntax", "Desc."),
            )]
            for (key, item) in self.sploit_list.items():
                DATA.append(table_print(
                    (key, item),
                ))
            if ASCII_ONLY:
                table = AsciiTable(DATA, "[ {0}{2}{1} ]".format(
                    color.END + color.BOLD,
                    color.END + color.RD,
                    "PHASE 2",
                ))
            else:
                table = SingleTable(DATA, "[ {0}{2}{1} ]".format(
                    color.END + color.BOLD,
                    color.END + color.RD,
                    "PHASE 2",
                ))
            print("\n" + color.RD + table.table + color.END + "\n")
        elif inp == "CONFIG":
            pass
        else:
            DATA = [table_print(
                ("Name", "Desc."),
            )]
            for (key, item) in self.list_sets.items():
                DATA.append(table_print(
                    (key, item),
                ))
            if ASCII_ONLY:
                table = AsciiTable(DATA, "[ {0}{2}{1} ]".format(
                    color.END + color.BOLD,
                    color.END + color.RD,
                    "SETS",
                ))
            else:
                table = SingleTable(DATA, "[ {0}{2}{1} ]".format(
                    color.END + color.BOLD,
                    color.END + color.RD,
                    "SETS",
                ))
            print("\n" + color.RD + table.table + color.END + "\n")

    def help_list(self):
        title = "list"
        description = """List elements of a set, or list all available
config sets."""
        syntax = "list [SET]"
        args = {"SET": "The set to list elements from."}
        examples = ["list", "list OPTIONS"]
        help_formatter(
            title, description, args=args, syntax=syntax,
            examples=examples,
        )

    def do_attack(self, inp):
        pass

    def help_attack(self):
        title = "attack"
        description = """Launch the configured attack on the selected
target."""
        further = ["{}set{} OPT VAL".format(color.BOLD, color.END)]
        help_formatter(title, description, further=further)


def shell_main():
    intro(shell=True)
    vailyn_shell = VailynShell()
    vailyn_shell.cmdloop()
