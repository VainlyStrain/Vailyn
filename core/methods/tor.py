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
import re
import random
import requests
import subprocess
from urllib.request import urlopen
import core.variables as vars
from core.colors import color


def presession():
    """
    Returns session for IP change verification
    """
    presess = requests.session()
    if vars.tor:
        presess.proxies["http"] = "socks5h://localhost:9050"
        presess.proxies["https"] = "socks5h://localhost:9050"
        presess.headers["User-agent"] = vars.user_agents[
            random.randrange(0, len(vars.user_agents))
        ]
    return presess


def torpipe(controller):
    """
    Detect if the Tor service is active and running
    """
    try:
        mac_os = False
        try:
            status = subprocess.run(
                ["systemctl", "status", "tor"],
                check=True,
                stdout=subprocess.PIPE,
            ).stdout
        except OSError:  # non-systemd distro
            status = subprocess.run(
                ["service", "tor", "status"],
                check=True,
                stdout=subprocess.PIPE
            ).stdout
        except OSError:  # macOS
            mac_os = True
            status = subprocess.run(
                ["brew", "services", "list"],
                check=True,
                stdout=subprocess.PIPE,
            ).stdout
        if "active (running)" in str(status) and not mac_os:
            return True
        elif re.match(
            ".*tor\s+started.*", str(status), flags=re.DOTALL,
        ) and mac_os:
            return True
        else:
            print(
                color.R + " [-] " + color.END
                + "Tor service not running. Aborting..."+color.END
            )
            return False
    except subprocess.CalledProcessError:
        print(
            color.R + " [-] " + color.END
            + "Tor service not installed or running. Aborting..."
            + color.END
        )
        return False


def init_check():
    """
    grab real attacker IP to verify if Tor works
    """
    ipaddr = urlopen("http://ip.42.pl/raw").read()
    vars.initip = str(ipaddr).split("'")[1]


def tor_check():
    """
    verify if Tor works by comparing current IP with IP from init_check()
    """
    s = presession()
    try:
        ipaddr = s.get("http://ip.42.pl/raw", timeout=vars.timeout).text
    except (requests.exceptions.Timeout, requests.exceptions.ConnectionError):
        sys.exit("Timeout at IP check.")
    if vars.initip.strip() != ipaddr:
        vars.torip = ipaddr
    else:
        print(
            color.R + " [-] " + color.END
            + "Tor Check failed: Real IP used. Aborting."
        )
        sys.exit(1)


def enable_tor(shell=True, sig_win=False, sig_lin=False):
    """
    enable the Tor service and exit program if failed
    """
    vars.tor = True
    try:
        init_check()
        acc = True
    except Exception:
        acc = False

    if acc or not vars.initip == "":
        if vars.is_windows:
            if shell:
                status = input(
                    color.END + " [?] Do you have the Tor service"
                    + " actively running? (enter if not) :> ",
                )
            elif sig_win:
                status = "y"
            else:
                return 420
            if status == "":
                sys.exit(" {}[-]{} Aborting.".format(color.R, color.END))
        else:
            p = torpipe(True)
            if not p:
                if shell:
                    start = input(
                        color.END+" [?] Do you want to start"
                        + " the Tor service? (enter if not) :> ",
                    )
                elif sig_lin:
                    start = "y"
                else:
                    return 1337
                if start != "":
                    try:
                        subprocess.run(["systemctl", "start", "tor"])
                        p = torpipe(True)
                    except OSError:  # non-systemd distro
                        subprocess.run(["service", "tor", "start"])
                        p = torpipe(True)
                    except OSError:  # macOS - requires brew
                        subprocess.run(["brew", "services", "start", "tor"])
                        p = torpipe(True)
                    except Exception as e:
                        sys.exit(e)
        tor_check()
        return 0
    else:
        sys.exit(
            "{} [-]{} Problems setting initial IP. Aborting.".format(
                color.R, color.END,
            )
        )
