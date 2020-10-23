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


import sys, re, random
import requests
import subprocess
from urllib.request import urlopen
import core.variables as vars
from core.colors import color


"""Returns session for IP change verification"""
def presession():
    presess = requests.session()
    if vars.tor:
        presess.proxies['http'] = 'socks5h://localhost:9050'
        presess.proxies['https'] = 'socks5h://localhost:9050'
        presess.headers['User-agent'] = vars.user_agents[random.randrange(0, len(vars.user_agents))]
    return presess

"""Detect if the Tor service is active and running"""
def torpipe(controller):
    try:
        macOS = False
        try:
            status = subprocess.run(['systemctl','status','tor'], check=True, stdout=subprocess.PIPE).stdout
        except OSError: #non-systemd distro
            status = subprocess.run(['service','tor','status'], check=True, stdout=subprocess.PIPE).stdout
        except OSError: #macOS
            macOS = True
            status = subprocess.run(['brew','services','list'], check=True, stdout=subprocess.PIPE).stdout
        if "active (running)" in str(status) and not macOS:
            return True
        elif re.match(".*tor\s+started.*", str(status), flags=re.DOTALL) and macOS:
            return True
        else:
            print(color.R + " [-] " + color.END + "Tor service not running. Aborting..."+color.END)
            return False
    except subprocess.CalledProcessError:
        print(color.R + " [-] " + color.END + "Tor service not installed or running. Aborting..."+color.END)
        return False

"""grab real attacker IP to verify if Tor works"""
def initcheck():
    ipaddr = urlopen('http://ip.42.pl/raw').read()
    vars.initip = str(ipaddr).split("'")[1]

"""verify if Tor works by comparing current IP with IP from initcheck()"""
def torcheck():
    #try:
    s = presession()
    try:
        ipaddr = s.get('http://ip.42.pl/raw', timeout=vars.timeout).text
    except (requests.exceptions.Timeout, requests.exceptions.ConnectionError):
        sys.exit("Timeout at IP check.")
    #ip = str(ipaddr).split("'")[1].strip()
    if vars.initip.strip() != ipaddr:
        vars.torip = ipaddr
    else:
        print(color.R + " [-] " + color.END + "Tor Check failed: Real IP used. Aborting.")
        sys.exit()
    #except:
    #    print(R + " [-] " + "\033[0m" + color.UNDERLINE + "\033[1m" + "IPcheck socket failure.")
    #    torcheck() 

def enableTor(shell=True, sigWin=False, sigLin=False):
    vars.tor = True
    try:
        initcheck()
        acc = True
    except:
        acc = False

    if acc or not vars.initip == "":
        if sys.platform.lower().startswith('win'):
            if shell:
                status = input(color.END+" [?] Do you have the Tor service actively running? (enter if not) :> ")
            elif sigWin:
                status = "y"
            else:
                return 420
            if status == "":
                sys.exit(" {}[-]{} Aborting.".format(color.R, color.END))
        else:
            p = torpipe(True)
            if not p:
                if shell:
                    start = input(color.END+" [?] Do you want to start the Tor service? (enter if not) :> ")
                elif sigLin:
                    start = "y"
                else:
                    return 1337
                if start != "":
                    try:
                        subprocess.run(["systemctl", "start", "tor"])
                        p = torpipe(True)
                    except OSError: #non-systemd distro
                        subprocess.run(["service", "tor", "start"])
                        p = torpipe(True)
                    except OSError: #macOS - requires brew
                        subprocess.run(["brew", "services", "start", "tor"])
                        p = torpipe(True)
                    except Exception as e:
                        sys.exit(e)
        torcheck()
        return 0
    else:
        sys.exit("{} [-]{} Problems setting initial IP. Aborting.".format(color.R, color.END))
